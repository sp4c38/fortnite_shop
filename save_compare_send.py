import arrow
import configparser
import io
import os
import requests

from PIL import Image

def get_stored_image(settings):
    # Gets the last stored image
    # The recent.info files stores which file was last stored in the backups directory
    recent_info = configparser.ConfigParser()
    recent_info.read(str(settings["recent_info"]))
    recent_stored_file = recent_info['recent_stored_file']['rct_srd_file']

    if not recent_stored_file:
        return None
    else:
        try:
            open(recent_stored_file)
        except:
            return None
        
        return Image.open(recent_stored_file)


def compare(recent_image, stored_image):
    # Return True if image changed and False if image hasn't changed

    if stored_image == None:
        return True

    if recent_image.tobytes() == stored_image.tobytes():
        return False
    else:
        return True

def save_image(settings, image):
    # Uses UTC timezone
    backup_dir = settings["backup_dir"].format(arrow.utcnow().format("DD-MM-YYYY"))
    backup_file = os.path.join(backup_dir, "final.png")
    
    os.makedirs(backup_dir, exist_ok=True)
    image.save(backup_file)

    recent_info = configparser.ConfigParser()
    recent_info.read(str(settings["recent_info"]))
    recent_info["recent_stored_file"]["rct_srd_file"] = backup_file
    with open(settings["recent_info"], "w") as file:
        recent_info.write(file)

def send_message(config, message):
    print("Sending message...")
    url = config["telegram"]["send_message_url"]

    data = {
        "chat_id": config["telegram"]["chat_id"],
        "text": message,
        "disable_notification": True,
    }

    requests.post(url=url, data=data)

def send_image(config, image):
    print("Sending image...")
    url = config["telegram"]["send_photo_url"]

    my_memory = io.BytesIO()
    image.save(my_memory, format="PNG")

    data = {
        "chat_id": config["telegram"]["chat_id"],
    }
    files = {
        "photo": my_memory.getvalue(),
    }

    requests.post(url=url, data=data, files=files)

def send_video(config, vid_dest):
    print("Sending video...")
    url = config["telegram"]["send_video_url"]

    data = {
        "chat_id":config["telegram"]["chat_id"],
        "disable_notification": True,
    }
    files = {
        "video": open(vid_dest, "rb").read(), 
    }

    requests.post(url=url, data=data, files=files)

