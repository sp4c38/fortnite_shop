import io
import requests

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

def send_video(config, vid_path):
    print("Sending video...")
    url = config["telegram"]["send_video_url"]

    data = {
        "chat_id":config["telegram"]["chat_id"],
        "disable_notification": True,
    }
    files = {
        "video": open(vid_path, "rb").read(), 
    }

    requests.post(url=url, data=data, files=files)