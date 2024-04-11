from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import crop
import time
import os

class VideoProcessor:
    def cropVideo(src, dest, x, y, h, w):
        clip = VideoFileClip(src)
        cropped_clip = crop(clip, x1=x, y1=y, width=w, height=h)
        cropped_clip.write_videofile(dest)

    def get_most_recent_fdmdownload():
        downloads_folder = os.path.expanduser("~/Downloads")  # Path to the Downloads folder

        while True:
            files = os.listdir(downloads_folder)
            for file in files:
                if file.endswith(".mp4.fdmdownload"):
                    return os.path.join(downloads_folder, file)
            time.sleep(1)  # Wait for 1 second

    # Function to convert .fdmdownload file to its corresponding MP4 file
    def convert_fdmdownload_to_mp4(fdmdownload_path):
        mp4_path = fdmdownload_path.replace(".fdmdownload", "")
        while not os.path.exists(mp4_path):
            time.sleep(1)  # Wait for 1 second
        # os.rename(fdmdownload_path, mp4_path)
        return mp4_path