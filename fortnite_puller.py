import datetime
import glob
import io
import os
import random
import requests
import hashlib
import shutil
import tempfile

from PIL import Image
from os.path import expanduser

# Put in credentials file later
chat_id = '-1001269378894'
send_photo_link = 'https://api.telegram.org/bot723477855:AAEPsApC9-UXtWZ7QWZxndvRuY8ZXQoXM1g/sendPhoto'

shop_url = 'https://fnbr.co/api/shop'
headers = {
  'x-api-key': 'dcf4fb2e-5e42-4938-9706-33e9283089e1'
}

# open requests session (more effectiv than to open one each time needed)
requests_session = requests.Session()

# Change some stuff here if ya want to

# Some general settings
store_path = expanduser(os.path.join('~', 'Documents', 'fortnite_shop'))
store_path_final = expanduser(os.path.join('~', 'Documents', 'fortnite_shop' , '{0}', 'final.png'))

# Settings for images next to each other in a row
row_images_next_to_each_other = 4 # How many images shall be next to each other?
width = 512 # The width of each individual image / Width should be: width=height
height = 512 # The height of each individual image / height should be: height=width
# Settings for the final image
final_img_bg = (255,102,0) # Please specify as RGB or RGBA

images = []
img_links = []

# Give api key with in header (must be 'headers' in request)
# Pulls json from api site with credentials and gets needed information

data = (requests_session.get(url=shop_url, headers=headers)).json()
for item in data['data']['featured']:
    img_links.append(item['images']['icon'])

for item in data['data']['daily']:
    img_links.append(item['images']['icon'])


# Creates name for directory (with date)
date = datetime.date.today().timetuple()
dir_name = "_".join([str(date.tm_mday), str(date.tm_mon), str(date.tm_year)])

if not os.path.exists(path=(f'{store_path}/{dir_name}')):
    os.makedirs(name=(f'{store_path}/{dir_name}'))

print('Downloading...')
for link in img_links:
    # Saves image from website as PIL.Image
    print(link)
    images.append(Image.open(io.BytesIO(requests.get(url=link).content)))


def first_items(items_list, number):
    x = 0
    first_items = []
    
    for item in items_list[slice(number)]:
        first_items.append(items_list.pop(items_list.index(item)))
    
    return first_items

def img_to_row(img_list):
    row_img = Image.new(mode='RGBA', size=((len(img_list)*width), height), color=final_img_bg)
    
    x_paste=0
    y_paste=0
    
    for image in img_list:
        row_img.paste(im=image, box=(x_paste, y_paste))
        x_paste += width

    return row_img

def rows_to_one(rows):
    result_img = Image.new(mode='RGBA',color=final_img_bg,\
                            size=((row_images_next_to_each_other*width),height*len(rows)))
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
        send_img_as_telegram_message()

def edit_single_image(image_2_edit):
    image_2_edit = image_2_edit.resize(size=(width,height))

    x_paste = 0
    y_paste = 0

    edited_image = Image.new(size=(width, height), color=final_img_bg, mode='RGBA')
    edited_image.paste(im=image_2_edit, box=(0,0), mask=image_2_edit)
    
    return edited_image


images_sliced = []
row_imgs = []

for image in images:
    images[images.index(image)] = edit_single_image(image_2_edit=image)

while len(images) > 0:
    images_sliced.append(first_items(items_list=images, number=row_images_next_to_each_other))

for item in images_sliced:
    row_imgs.append(img_to_row(img_list=item))

final = rows_to_one(rows=row_imgs)

temp_file_path = tempfile.mkstemp(suffix='.png')[1]
final.save(fp=temp_file_path)

# Checks if the latest stored image is the same as this one pulled
# If so, don't have tp send it again
check_if_changed(final_img=final, saved_imgs_path=store_path)
os.remove(temp_file_path)