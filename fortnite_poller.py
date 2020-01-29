# normal imports (sorted alphabetical)
import arrow
import configparser
import datetime
import requests
import tempfile

# from... imports
from io import BytesIO
from PIL import Image,ImageDraw,ImageFont

# Import files
import image
import video
import telegram
import merge_pictures

from settings import settings

class ShopItem(): # Can't be named Image because it would overwrite the Image class from PIL
    def __init__(self, image=None, name=None, rarity=None, price=None, video=None): # Consider key word arguments for better overview of the program
        self.image = image
        self.name = name
        self.rarity = rarity
        self.price = price
        self.video = video

def get_images(config):

    headers = {
        'x-api-key':config['fortnite']['api-key'],
    }

    req = requests.Session() # requests only needed in this function

    data = req.get(url=config['fortnite']['request_url'], headers=headers).json()
    date = arrow.get(data['data']['date']).format("HH:mm D.M.YYYY") # Time shop is from

    imageobjs = [] # A list with all Image object

    for item in data['data']['featured']: # Featured items, most multiple days in shop
        image_object = ShopItem()
        
        if item['images']['featured']:
            image_link = item['images']['featured']
        else:
            image_link = item['images']['icon']

        if item['rarity']:
            image_object.rarity = item['rarity']
        if item['price']:
            image_object.price = item['price']
        if item['name']:
            image_object.name = item['name']
        
        print(f"Downloading {image_link}")

        image_object.image = Image.open(BytesIO(req.get(url=image_link).content)).convert('RGBA')
        image_object.image = merge_pictures.edit_single_image(settings=settings, imageobj=image_object)

        if item["history"]["occurrences"] == 1: # Only checks for video if item occured 1 time (this time is also counted)
            download_url = video.find_video(item=item, req_session=req, config=config)

            if download_url:
                # Returns a path to the video if it is new, returns False if it is not new
                image_object.video = video.check_save_video(item=item, url=download_url, settings=settings)


        imageobjs.append(image_object)

    for item in data['data']['daily']: # Daily items, mostly not multiple days in shop
        image_object = ShopItem()
        
        if item['images']['featured']:
            image_link = item['images']['featured']
        else:
            image_link = item['images']['icon']

        if item['rarity']:
            image_object.rarity = item['rarity']
        if item['price']:
            image_object.price = item['price']
        if item['name']:
            image_object.name = item['name']

        print(f"Downloading {image_link}")

        if item["history"]["occurrences"] == 1: # Only checks for video if item occured 1 time (this time is also counted)
            download_url = video.find_video(item=item, req_session=req, config=config)

            if download_url:
                # Returns a path to the video if it is new, returns False if it is not new
                image_object.video = video.check_save_video(item=item, url=download_url, settings=settings)

        image_object.image = Image.open(BytesIO(req.get(url=image_link).content))
        image_object.image = merge_pictures.edit_single_image(settings=settings, imageobj=image_object)

        imageobjs.append(image_object)

    req.close()

    return date, imageobjs


def main():
    config = configparser.ConfigParser() # Don't mix it up with settings 
    config.read(str(settings['config_file'])) # Config file stores confidential data

    date, data_obj = get_images(config=config)
    objsplit = merge_pictures.items_split(items_list=data_obj, number=settings['images_in_row'])
    rowimgs = merge_pictures.imgs_to_rows(img_list=objsplit, settings=settings)
    final_image = merge_pictures.rows_to_final(settings=settings, rows=rowimgs)

    stored_image = image.get_stored_image(settings=settings)
    image_updated = image.image_changed(now_img=final_image, strd_img=stored_image)
    
    if image_updated:
        print("Shop image updated.")
        telegram.send_message(config=config, message=f"Shop von: {date}") # A message, with the date the shop is from
        image.save_image(settings=settings, image=final_image) # Save final image to backups
        telegram.send_image(config=config, image=final_image) # Send final image via Telegram
    elif not image_updated:
        print("Same image.")
    
    for shopobj in data_obj:
        if shopobj.video:
            print(f"A video for \"{shopobj.name}\" was found.")
            telegram.send_video(config=config, vid_path=shopobj.video)
  
if __name__ == '__main__':
    main()