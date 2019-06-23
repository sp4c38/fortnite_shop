import datetime
import os
import random
import requests
import shutil
import tempfile

from os.path import expanduser

chat_id = '-1001269378894'
send_photo_link = 'https://api.telegram.org/bot723477855:AAEPsApC9-UXtWZ7QWZxndvRuY8ZXQoXM1g/sendPhoto'
store_path = '~/Documents/fortnite_shop'

url = 'https://fortnite-api.theapinetwork.com/store/get'
headers = {
  'Authorization': '1b356241bf656c44c8ce44859be14391'
}

requests_session = requests.Session()
store_files = []

# Give api key with in header (must be 'headers' in request)
data = (requests_session.get(url, headers = headers)).json()
store_links = []

for item in data['data']:
    store_links.append(item['item']['images']['information'])

date = datetime.date.today().timetuple()
dir_created_date = "_".join([str(date.tm_mday), str(date.tm_mon), str(date.tm_year)])

shutil.rmtree((expanduser(store_path)+f'/{dir_created_date}'))

if not os.path.exists(path=(expanduser(f'{store_path}/{dir_created_date}'))):
    os.makedirs(name=(expanduser(f'{store_path}/{dir_created_date}')))

def generate_mkstemp():
    imagefile_path = ((tempfile.mkstemp(prefix='fn_', suffix='.png',
                        dir=(expanduser('{0}/{1}'.format(store_path, dir_created_date)))))[1])
    return imagefile_path

for link in store_links:
    imagefile_path = generate_mkstemp()
    while imagefile_path in store_files:
        imagefile_path = generate_mkstemp()
    store_files.append(imagefile_path)
    with open(imagefile_path, 'wb') as f:
        image = requests_session.get(url=link)
        f.write(image.content)
        print(f"Successfully wrote image to: {imagefile_path}")
        

for i in store_files:
    header = {
    'chat_id': chat_id
    }
    file = {
        'photo':open(i, 'rb')
    }
    requests.post(url=send_photo_link, data=header, files=file)
print("Send all photos successfully.")

