import arrow
import configparser
import io
import os
import requests

from PIL import Image

def get_stored_backup(settings):
    # Returns the most recent stored image as a PIL.Image object
    # The path to the most recent stored image is stored in a recent.info file (can also be named different)

    recent_info = configparser.ConfigParser()
    recent_info.read(str(settings["recent_info"]))
    recent_stored_img_names = [str(x) for x in recent_info['recent_stored_files']['rct_srd_image_names'].split(",")]
    
    if not recent_stored_img_names:
        return None
    else:
        return recent_stored_img_names


def image_changed(now_data, stored_data):
    # The program backup system works, with looking at the names from the last saved backup
    # and comparing them with the names from the stored_data

    # This is better than comparing a stored image with the current created image -> this can easily lead to mistakes in recognizing changes
 
    if now_data == stored_data:
        return False
    else:
        return True

def save_image(settings, image, names):
    # Uses UTC timezone
    backup_dir = settings["img_backup_dir"].format(arrow.utcnow().format("DD-MM-YYYY"))
    backup_path = os.path.join(backup_dir, "final.png")
    
    os.makedirs(backup_dir, exist_ok=True)
    image.save(backup_path)

    recent_info = configparser.ConfigParser()
    recent_info.read(str(settings["recent_info"]))

    recent_info["recent_stored_files"]["rct_srd_image_names"] = ",".join(names)

    with open(settings["recent_info"], "w") as file:
        recent_info.write(file)



