import glob
import os

import moviepy.editor as mp
from pytube import YouTube

global Session_info
Session_info = [0]

def dowlaod(link):
    try:
        yt = YouTube(link)
    except:
        print("Connection Error")
    Sound_files = yt.streams.filter()
    try:
        Sound = yt.streams.get_by_itag(17)
        Sound.download(filename="1.3gpp",output_path="Player_folder")
        #139 = mp4
        #249 = webm
    except:
        print("Some Error!")
    print('Task Completed!')

def extract_audio(Video_path, savename):
    clip = mp.VideoFileClip(f"Player_folder\{Video_path}")
    clip.audio.write_audiofile(f"Player_folder\{savename}")
    clip.close()

def clear_folder(Things_to_remove):
    files = glob.glob(f'Player_folder/{Things_to_remove}')
    for f in files:
        os.remove(f)

def Full_download(link):
    clear_folder("1.*")
    dowlaod(link)
    extract_audio("1.3gpp", "1.wav")