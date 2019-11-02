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

# open requests session (more effectiv than to open one each time needed)
requests_session = requests.Session()

# Change some stuff here if ya want to

# Some general settings
rarity_grades = {
    'uncommon': Image.open(expanduser(os.path.join('~','Documents','fortnite_shop','backgrounds','green_uncommon.png'))), #green
    'common':Image.open(expanduser(os.path.join('~','Documents','fortnite_shop','backgrounds','gray_common.png'))), # gray
    'rare': Image.open(expanduser(os.path.join('~','Documents','fortnite_shop','backgrounds','blue_rare.png'))), # blue
    'epic': Image.open(expanduser(os.path.join('~','Documents', 'fortnite_shop','backgrounds','purple_epic.png'))), # purple
    'legendary': Image.open(expanduser(os.path.join('~','Documents','fortnite_shop','backgrounds','orange_legendary.png'))) # orange
}

text_color_for_rarity = {
    'uncommon': (255,215,0), #green
    'common': (100,0,255), # gray
    'rare': (255,100,0),  # blue
    'epic': (100,255,0), # purple
    'legendary':  (255,0,100), # orange 
}
default_text_color_for_rarity = (102,255,255)

backups_store_path = expanduser(os.path.join('~', 'Documents', 'fortnite_shop', 'backups'))
store_path_final = expanduser(os.path.join('~', 'Documents', 'fortnite_shop' , 'backups', '{0}', 'final.png'))

text_font_path = expanduser(os.path.join('~', 'Documents', 'fortnite_shop', 'fonts', 'Lato-Bold.ttf')) # Please set as .ttf file
         
# Settings for text (for each image)
text_color = (255,255,255)

name_text_size = 30
text_size = 40 #  Will size the vbucks image according to this setting

spacing_to_top_vbucks_image = 20
spacing_to_top_price_text = 15
spacing_to_top_name_text = 70

spacing_to_side = 2 # spacing to edge of the vbucks image in pixel (will adjust the text field automatically)

spacing_to_vbucks_image = 10 # The space which the price text is situated next to the vbucks image
vbucks_img_path = expanduser(os.path.join('~', 'Documents', 'fortnite_shop', 'data', 'vbucks_icon', 'icon_vbucks.png'))


# Settings for images next to each other in a row
row_images_next_to_each_other = 4 # How many images shall be next to each other in one row?
                                  # If there are too less images in one row so that it still looks comfortable (that there
                                  # aren't too many rows, the program will automatically increase the amout of 
                                  # images next to each other in one row

width = 512 # The width of each individual image / Width should be: width=height
height = 512 # The height of each individual image / height should be: height=width
# Settings for the final image
bg_not_found_bg = (255,102,0) # Is used when there is no background image found / Please specify as RGB or RGBA
border_color = (255,255,255) # Please specify as RGB, RGBA will not work

# Give api key with in header (must be 'headers' in request)
# Pulls json from api site with credentials and gets needed information

data = (requests_session.get(url=shop_url, headers=headers)).json()

image_data = [] # Items in list as NamedTuple

for item in data['data']['featured']:
    part_data = NamedTuple('image_data', [('image', str),('rarity', str),('price', str),('name', str)])

    if item['images']['featured']:
        part_data.image = item['images']['featured']
    else:
        part_data.image = item['images']['icon']

    part_data.rarity = item['rarity']
    part_data.price = item['price']
    part_data.name = item['name']

    image_data.append(part_data)

for item in data['data']['daily']:
    part_data = NamedTuple('image_data', [('image', str),('rarity', str),('price', str),('name', str)])
    
    if item['images']['featured']:
        part_data.image = item['images']['featured']
    else:
        part_data.image = item['images']['icon']


    part_data.img_link = item['images']['icon']
    
    part_data.rarity = item['rarity']
    part_data.price = item['price']
    part_data.name = item['name']

    image_data.append(part_data)

# Increases the amout of images next to each other -> to not have too many rows

if len(image_data) > row_images_next_to_each_other*4:
    row_images_next_to_each_other = int(row_images_next_to_each_other*1.5)

# Creates name for directory (with date)
date = datetime.date.today().timetuple()
dir_name = "_".join([str(date.tm_mday), str(date.tm_mon), str(date.tm_year)])

if not os.path.exists(path=(f'{backups_store_path}/{dir_name}')):
    os.makedirs(name=(f'{backups_store_path}/{dir_name}'))

print("Polling...")
for i in image_data:
    print(i.image)
    i.image = Image.open(io.BytesIO(requests.get(url=i.image).content))

print("Download/Downloads successfully completed.")


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
os.remove(temp_file_path)
