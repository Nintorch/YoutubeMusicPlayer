from pytube import YouTube, Search
import os
from pyffmpeg import FFmpeg
from urllib.request import urlretrieve

# We're using FFmpeg to convert the downloaded mp4 to ogg
ff = FFmpeg()


class Track:
    def __init__(self, yt):
        yt: YouTube
        self.title = yt.title
        self.filename = ""
        self.thumbnail = ""


# dummy logging function
# main.py replaces it with proper function
def log(s):
    print(s)


# Make sure the tracks folder exists
folder = "tracks"
if not os.path.exists(folder):
    os.makedirs(folder)


# Download the requested track
def download(path):
    yt: YouTube
    yt = Search(path).results[0]

    track = Track(yt)

    track.filename = os.path.join(folder,yt.video_id+".ogg")
    track.thumbnail = os.path.join(folder,yt.video_id+".jpg")

    if not os.path.exists(track.filename):
        log("Downloading %s" % yt.title)
        yt.streams.filter(only_audio=True).first().download(filename="%s.mp4" % yt.video_id)
        log("Converting video to audio")
        ff.convert("%s.mp4" % yt.video_id,track.filename)
        os.remove("%s.mp4" % yt.video_id)

        # Thumbnail
        urlretrieve(yt.thumbnail_url,track.thumbnail)

    return track
