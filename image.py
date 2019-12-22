import arrow
import configparser
import io
import os
import requests

from PIL import Image

def get_stored_image(settings):
    # Returns the most recent stored image as a PIL.Image object
    # The path to the most recent stored image is stored in a recent.info file (can also be named different)

    recent_info = configparser.ConfigParser()
    recent_info.read(str(settings["recent_info"]))
    recent_stored_img_path = recent_info['recent_stored_files']['rct_srd_image']

    if not recent_stored_img_path:
        return None
    else:
        try:
            return Image.open(recent_stored_img_path)
        except:
            return None


def image_changed(now_img, strd_img):
    # now_img and strd_img must be a PIL.Image object
    # Checks if now_img is different from strd_img, returns True if this is the case and False if not

    if strd_img == None:
        return True

    if now_img.tobytes() == strd_img.tobytes():
        return False
    elif now_img.tobytes() != strd_img.tobytes():
        return True

def save_image(settings, image):
    # Uses UTC timezone
    backup_dir = settings["img_backup_dir"].format(arrow.utcnow().format("DD-MM-YYYY"))
    backup_path = os.path.join(backup_dir, "final.png")
    
    os.makedirs(backup_dir, exist_ok=True)
    image.save(backup_path)

    recent_info = configparser.ConfigParser()
    recent_info.read(str(settings["recent_info"]))

    recent_info["recent_stored_files"]["rct_srd_image"] = backup_path

    with open(settings["recent_info"], "w") as file:
        recent_info.write(file)



