import datetime
import os
import random
import requests
import tempfile

from os.path import expanduser

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

if not os.path.exists(path=(expanduser(f'~/Documents/fortnite_shop/{dir_created_date}'))):
    os.makedirs(name=(expanduser(f'~/Documents/fortnite_shop/{dir_created_date}')))

def generate_mkstemp():
    imagefile_path = ((tempfile.mkstemp(prefix='fn_', suffix='.png',
                        dir=(expanduser('~/Documents/fortnite_shop/{0}'.format(dir_created_date)))))[1])
    return imagefile_path

for link in store_links:
    imagefile_path = generate_mkstemp()
    while imagefile_path in store_files:
        imagefile_path = generate_mkstemp()

    with open(imagefile_path, 'wb') as f:
        image = requests_session.get(url=link)
        f.write(image.content)
    print(f"Successfully wrote image to: {imagefile_path}")  

print(store_files)
    