from inspect import currentframe
from msilib.schema import Media
from sys import _current_frames
from turtle import window_width
from winsound import PlaySound
from xml.dom.pulldom import CHARACTERS
import PIL.Image

import numpy as np
import time
import cv2
import os
import random
import logging
import string
import re
import ffpyplayer
import multiprocessing
# bad apple wait 32 and interval 2/69 size 100
# b* wait 38 and interval 2/67,3/74 size 170
#homunculus wait 30 interval 3/92 size 170
ASCII_chars=["@","#","S","%","?","*","+",";",":",",","."]
frame_interval=3/74

class Convertor:
    @staticmethod
    def resize_image(image,new_width=170):
        width,height=image.size
        ratio=height/width
        new_height=int(new_width*ratio)
        resized_image=image.resize((new_width,new_height))
        return(resized_image)
    @staticmethod
    def grayify(image):
        grayscale_image=image.convert("L")
        return(grayscale_image)

    @staticmethod
    def pixels_to_ascii(image):
        pixels=image.getdata()
        characters="".join([ASCII_chars[pixel//25]for pixel in pixels])
        return(characters)

    def __init__(self,path,new_width=170):
        
        #path=input("new frame:\n")
        try:
            image=PIL.Image.open(path)
        except:
            print(path," is not a valid path for frame\n")
        new_image_data  = self.pixels_to_ascii(self.grayify(self.resize_image(image)))

        pixel_count=len(new_image_data)
        ascii_image="\n".join(new_image_data[i:(i+new_width)]for i in range(0,pixel_count,new_width))
    
        print(ascii_image)


def video_convertor(video_path):

    vid=cv2.VideoCapture(video_path)
    currentframe=0

    if not os.path.exists('dataAHD'):
        os.makedirs('dataAHD')

    power=10;
    count=1
    while(True):
        succes,frame=vid.read()

        cv2.imshow("output",frame)
        currentstring=str(currentframe)
        cv2.imwrite('./dataAHD/frame'+currentstring+'.jpg',frame)
        currentframe+=1

        if cv2.waitKey(1)& 0xFF==ord('q'):
            break
    vid.release()
    cv2.destroyAllWindows()

from ffpyplayer.player import MediaPlayer

def show_video():
    vid=cv2.VideoCapture(video_path)
    player=MediaPlayer(video_path)
    while(True):

        succes,frame=vid.read()
        audio_frame, val = player.get_frame()

        cv2.imshow("output",frame)


        if cv2.waitKey(38)& 0xFF==ord('q'):
            break
        if val != 'eof' and audio_frame is not None:
            #audio
            img, t = audio_frame
    vid.release()
    cv2.destroyAllWindows()


def generate_video():
    
    path="C://Users//anton//source//repos//AsciiProject//AsciiProject//dataO"
    dir_list=os.listdir(path)
    dir_list.sort(key=lambda f: int(re.sub('\D', '', f)))
    count=0

    for frame in dir_list:
        #frame="C://Users//anton//source//repos//AsciiProject//AsciiProject//data//frame1.jpg"

        time_start=time.time()
        currentframe=path+"//"+frame
        Convertor(currentframe)
        #print(currentframe)
        time_end=float(time.time()-time_start)
        time.sleep(frame_interval-time_end)
        #time.sleep(0.0255)
        #clear = lambda: os.system('cls')
        #clear()

    #Convertor(currentframe)
    #frame1=Convertor("C://Users//anton//source//repos//AsciiProject//AsciiProject//data//frame1.jpg")


video_path="overlord.mp4"
ASCII_chars.sort(reverse=True)
if __name__ == '__main__':
    try:
        #video_convertor(video_path)
        pass
    except:
        pass
    video_generation=multiprocessing.Process(target=generate_video)
    video_show      =multiprocessing.Process(target=show_video)
    video_generation.start()
    video_show.start()
    video_generation.join()
    video_show.join()

