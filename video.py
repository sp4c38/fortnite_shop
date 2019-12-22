import arrow
import io
import os
import subprocess
import youtube_dl


from bs4 import BeautifulSoup


def find_video(item, req_session, config):
    # Finds the video url, if no video exists None is returned

    check_url = os.path.join(config["fortnite"]["base_url"],item['type'],item['slug']) # Video only shows on specific site, can't get video link with api
    raw_html = req_session.get(check_url).text

    bs = BeautifulSoup(raw_html, "html.parser")
    video = bs.find_all("iframe")

    if video:
        return video[0]["src"]
    else:
        return None

def check_save_video(item, url, settings):
    # First: Check if the video is new (is not in the video backup directory)
    # Second: If new return the path of the video and save the video, if not new return False

    destination_dir = f"{settings['vid_backup_dir']}".format(arrow.utcnow().format("DD-MM-YYYY"))
    destination_path = os.path.join(destination_dir, f"{item['id']}.mp4")

    if os.path.isfile(destination_path):
        return False

    elif not os.path.isfile(destination_path):
        os.makedirs(destination_dir, exist_ok=True)

        ydl_opts = {
            "format":"mp4",
            "outtmpl": destination_path,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return destination_path
