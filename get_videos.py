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

def get_video(item, url, settings):
    destination = f"{settings['video_cache_path']}/{item['id']}.mp4"

    ydl_opts = {
        "format":"mp4",
        "outtmpl":destination,
    }
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return destination