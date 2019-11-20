import configparser
import datetime
import glob
import hashlib
import io
import os
import random
import requests
import shutil
import sys
import tempfile

from os.path import expanduser
from PIL import Image,ImageDraw,ImageFont
from typing import NamedTuple

# Import files
import settings
import merge_pictures

# image_data now images

class ShopItem(): # Can't be named Image because it would overwrite the Image class from PIL
    def __init__(self, image=None, name=None, rarity=None, price=None): # Consider key word arguments for better overview of the program
        self.image = image
        self.name = name
        self.rarity = rarity
        self.price = price

def get_images(config=None):

    headers = {
        'x-api-key':config['fnbr_api']['api-key'],
    }

    req = requests.Session() # requests only needed in this function

    data = req.get(url=config['fnbr_api']['request_url'], headers=headers).json()

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
        
        print(f"Downloading {image_link}...")
        image_object.image = Image.open(io.BytesIO(req.get(url=image_link).content))

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
        image_object.image = Image.open(io.BytesIO(req.get(url=image_link).content))

        imageobjs.append(image_object)

    return imageobjs

def main():
    config = configparser.ConfigParser() # Don't mix it up with settings 
    config.read(str(settings.settings['config_file'])) # Settings file stores confidential data

    images = get_images(config)
    import IPython;IPython.embed()



if __name__ == '__main__':
    main()



# date = datetime.date.today().timetuple()
# dir_name = "_".join([str(date.tm_mday), str(date.tm_mon), str(date.tm_year)])

# if not os.path.exists(path=(f'{backups_store_path}/{dir_name}')):
#     os.makedirs(name=(f'{backups_store_path}/{dir_name}'))










"""
def items_sliced(items_list, number): 
    items_sliced = []

    while len(items_list) > 0:
        cache = []
        for item in items_list[slice(number)]:
            cache.append(item)
            items_list.pop(items_list.index(item))
        items_sliced.append(cache)

    return items_sliced


def send_img_as_telegram_message():
    files = {
        'photo':open(os.path.join(store_path_final.format(dir_name)),'rb')
    }
    header = {
        'chat_id':chat_id,
    }
    print("Sending telegram message (image).")
    requests.post(url=send_photo_link, data=header, files=files)

def check_if_changed(final_img, saved_imgs_path):
    # First get the latest created directory and than in this directory to latest created file
    dirs = glob.glob(os.path.join(saved_imgs_path, '*'))
    newest_dir = max(dirs, key=(os.path.getctime))
    files = glob.glob(os.path.join(newest_dir, '*'))

    if not files:
        newest_file = sorted(files, key=os.path.getmtime, reverse=True)
        saved_file_hash = None
    else:
        newest_file = sorted(files, key=os.path.getmtime, reverse=True)[0]
        saved_file_hash = hashlib.sha256(open(newest_file, 'rb').read()).hexdigest()

    pulled_file_hash = hashlib.sha256(open(temp_file_path, 'rb').read()).hexdigest()

    if saved_file_hash == pulled_file_hash:
        print("No new fortnite shop found. Still the same.")
    else:
        print("Found new fortnite shop.")
        final.save(fp=store_path_final.format(dir_name))
        # send_img_as_telegram_message()


for i in image_data:
    image_data[image_data.index(i)].image = edit_single_image(single_image_data=i)

image_data = items_sliced(items_list=image_data, number=row_images_next_to_each_other)

row_imgs = []
for items_in_list in image_data:
    row_imgs.append(imgs_to_row(img_list=items_in_list))

final = rows_to_one(rows=row_imgs)

temp_file_path = tempfile.mkstemp(suffix='.png')[1]
final.save(fp=temp_file_path)

# Checks if the latest stored image is the same as this one pulled
# If so, don't have tp send it again
check_if_changed(final_img=final, saved_imgs_path=backups_store_path)
os.remove(temp_file_path)"""
