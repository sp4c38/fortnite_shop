import configparser
import datetime
import requests
import tempfile

from io import BytesIO
from PIL import Image,ImageDraw,ImageFont

# Import files
import get_videos
import merge_pictures
import save_compare_send

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
            video  = get_videos.find_video(item=item, req_session=req, config=config)
            if video:
                image_object.video = get_videos.get_video(item=item, url=video, settings=settings)
            else:
                image_object.video = None

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

        print(f"Downloading {image_link}...")

        if item["history"]["occurrences"] == 1: # Only checks for video if item occured 1 time (this time is also counted)
            video  = get_videos.find_video(item=item, req_session=req, config=config)
            if video:
                image_object.video = get_videos.get_video(item=item, url=video, settings=settings)
            else:
                image_object.video = None

        image_object.image = Image.open(BytesIO(req.get(url=image_link).content))
        image_object.image = merge_pictures.edit_single_image(settings=settings, imageobj=image_object)

        imageobjs.append(image_object)

    req.close()

    return imageobjs


def main():
    config = configparser.ConfigParser() # Don't mix it up with settings 
    config.read(str(settings['config_file'])) # Config file stores confidential data

    images = get_images(config=config)
    imgsliced = merge_pictures.items_sliced(items_list=images, number=settings['images_in_row'])
    rows = merge_pictures.imgs_to_rows(img_list=imgsliced, settings=settings)
    final_image = merge_pictures.rows_to_final(settings=settings, rows=rows)

    stored_image = save_compare_send.get_stored_image(settings=settings)
    updated = save_compare_send.compare(recent_image=final_image, stored_image=stored_image)
    
    if not updated:
        print("Same shop.")
    elif updated:
        print("Shop updated.")
        save_compare_send.save_image(settings=settings, image=final_image) # Save final image to backups
        save_compare_send.send_image(config=config, image=final_image) # Send final image via Telegram
        for img in images:
            if img.video:
                save_compare_send.send_video(config=config, vid_dest=img.video)
  
if __name__ == '__main__':
    main()