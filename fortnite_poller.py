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
#.kmjwertfgioj
# A monster asks 'trick or treat'
from os.path import expanduser
from PIL import Image,ImageDraw,ImageFont
from typing import NamedTuple

# Put in credentials file later

chat_id = '-340145564'

send_photo_link = 'https://api.telegram.org/bot723477855:AAE4qRTIO_sfXTYbZZ3OJwk_CZPmGIOqLyA/sendPhoto'

shop_url = 'https://fnbr.co/api/shop'
headers = {
  'x-api-key': 'dcf4fb2e-5e42-4938-9706-33e9283089e1'
}

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

def imgs_to_row(img_list):
    row_img = Image.new(mode='RGBA', size=((len(img_list)*width), height))
    
    x_paste=0
    y_paste=0

    for item in img_list:
        row_img.paste(im=item.image, box=(x_paste, y_paste))
        x_paste += width


    return row_img

def rows_to_one(rows):
    result_img = Image.new(mode='RGBA', color=bg_not_found_bg, size=((row_images_next_to_each_other*width),height*len(rows)))
    x_paste=0
    y_paste=0
    
    for image in rows:
        result_img.paste(im=image, box=(x_paste,y_paste))
        y_paste += height
    
    return result_img

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

def edit_single_image(single_image_data):
    single_image_data.image = single_image_data.image.resize(size=(width,height))
    
    x_paste = 0
    y_paste = 0

    if not os.path.exists(text_font_path):
        print(f"Font path \'{text_font_path}\' doesn't exist.")
        sys.exit(1)

    img_elements = Image.new(mode='RGBA', size=(width,height))
    img_elements.paste(single_image_data.image)
    # Add v-bucks price for shop item
    data_box = Image.new(mode='RGBA', size=(width,height))
    vbucks_icon = Image.open(fp=vbucks_img_path)
    vbucks_icon = vbucks_icon.resize(size=(text_size,text_size))

    image_position = (spacing_to_side, spacing_to_top_vbucks_image)
    vbucks_text_position = ((spacing_to_side+vbucks_icon.width+spacing_to_vbucks_image), spacing_to_top_price_text)
    
    draw = ImageDraw.Draw(img_elements)
    font = ImageFont.truetype(font=text_font_path, size=text_size)

    # Draw vbucks image and price text
    img_elements.paste(im=vbucks_icon, box=image_position)
    draw.text(xy=vbucks_text_position, text=single_image_data.price, fill=text_color, font=font)
    
    # Draw item name according to if there is enough space (will draw every time, just different text size, or with wordwrap)
    if single_image_data.name:
        item_name = single_image_data.name
        spilted_name = item_name.split(' ')
        name_text_position = {'spacing_to_side': spacing_to_side, 'spacing_to_top':spacing_to_top_name_text}

    for word in spilted_name:
        if single_image_data.rarity in rarity_grades:
            text_color_2 = text_color_for_rarity[single_image_data.rarity]
        else:
            text_color_2 = default_text_color_for_rarity
        draw.text(xy=(name_text_position['spacing_to_side'], name_text_position['spacing_to_top']),\
         text=word, fill=text_color_2, font=font)
        name_text_position['spacing_to_top'] += text_size

    # Has to be pasted again on a new image so that the mask option works correctly (this type
    # of bug would only happen on some images (here not anymore (because it was fixed)))
    
    # Set background color (dependet on the rarity of the shop item (image))
    
    if single_image_data.rarity in rarity_grades:
        bg_image = Image.new(size=(width, height), mode='RGBA')
        rarity_bg_img = rarity_grades[single_image_data.rarity]
        rarity_bg_img = rarity_bg_img.resize(size=(width,height))
        bg_image.paste(im=rarity_bg_img, box=(0,0))
    else:
        rarity_bg_img = bg_not_found_bg
        bg_image = Image.new(size=(width, height),color=rarity_bg_img, mode='RGBA')

    # Draw border
    draw = ImageDraw.Draw(bg_image)
    draw.rectangle(xy=((0,0), (width,height)), outline=border_color, width=2)
    
    bg_image.paste(im=img_elements, box=(10,0), mask=img_elements)

    return bg_image


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
