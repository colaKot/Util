#!/usr/bin/python
# -*- coding: gbk -*
import os
import sys
import re
import chardet
from PIL import Image
import ffmpeg
from moviepy.video.io.VideoFileClip import VideoFileClip

path = sys.path[0]


def exte(a, *endstring):
    array = map(a.endswith, endstring)
    if True in array:
        return True
    else:
        return False

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']


def make_thumb():
    for dirpath, dirnames, filenames in os.walk(path):
        if dirpath.find("dfdf") < 0 and dirpath.find("dfdf") < 0:
            for name in filenames:
                if exte(name, type):
                    try:
                        videopath = os.path.join(dirpath, name)
                        videoname = os.path.splitext(name)[0]
                        outputname = os.path.join(dirpath, videoname)
                        outputname2 = os.path.join(dirpath, videoname+".jpg")
                        if not os.path.exists(outputname2):
                            clip = VideoFileClip(videopath)
                            width = clip.w
                            height = clip.h
                            showtime = clip.duration
                            if width>height:
                                num = 4
                                row = 2
                                line = 2
                                if showtime > 3600:
                                    num = 9
                                    row = 3
                                    line = 3
                                elif showtime < 10 and showtime > 1:
                                    num = 1
                                    row = 1
                                    line = 1
                                elif showtime < 1:
                                    print("short_"+str(showtime)+"_"+str(outputname2))
                                    continue

                                showtime2 = int(showtime/num)

                                nowtime = 1
                                for i in range(row):
                                    for j in range(line):
                                        shell = 'ffmpeg -y -hwaccel dxva2 -ss %s -i "%s" -f image2  -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2" -frames 1 "%s_img_%s_%s.jpg"' % (
                                        nowtime, videopath, outputname, i, j)
                                        os.system(shell)
                                        nowtime = nowtime + showtime2

                                print(str(showtime)+"_"+str(showtime2)+"_"+str(num))

                                toImage = Image.new('RGB', (2560, 1440))
                                if num == 6:
                                    toImage = Image.new('RGB', (3840, 1440))
                                elif num == 9:
                                    toImage = Image.new('RGB', (3840, 2160))
                                elif num == 1:
                                    toImage = Image.new('RGB', (1280, 720))

                                for i in range(row):
                                    for j in range(line):
                                        temp_img_path = '%s_img_%s_%s.jpg' % (outputname, i, j)
                                        if not os.path.exists(temp_img_path):
                                            continue
                                        pic_fole_head = Image.open(temp_img_path)
                                        toImage.paste(pic_fole_head, box=(j * 1280, i * 720))
                                        
                                toImage.save('%s.jpg' % (outputname))
                            else:
                                num = 5
                                row = 1
                                line = 5
                                if showtime > 3600 and showtime < 5400:
                                    num = 10
                                    row = 2
                                    line = 5
                                elif showtime >= 5400:
                                    num = 10
                                    row = 2
                                    line = 5
                                elif showtime > 0 and showtime < 60:
                                    num = 4
                                    row = 1
                                    line = 4
                                elif showtime < 1:
                                    print("short_"+str(showtime)+"_"+str(outputname2))
                                    continue

                                showtime2 = int(showtime/num+1)

                                nowtime = 5
                                for i in range(row):
                                    for j in range(line):
                                        shell = 'ffmpeg -y  -hwaccel dxva2 -ss %s -i %s -f image2 -vf "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(oh-ih)/2:(ow-iw)/2" -frames 1 %s_img_%s_%s.jpg' % (
                                            nowtime, videopath, outputname, i, j)
                                        os.system(shell)
                                        nowtime = nowtime + showtime2

                                print(str(showtime)+"_"+str(showtime2)+"_"+str(num))

                                toImage = Image.new('RGB', (2880, 1280))
                                if num == 5:
                                    toImage = Image.new('RGB', (3600, 1280))
                                elif num == 10:
                                    toImage = Image.new('RGB', (3600, 2560))
                                elif num == 1:
                                    toImage = Image.new('RGB', (720, 1280))

                                for i in range(row):
                                    for j in range(line):
                                        temp_img_path = '%s_img_%s_%s.jpg' % (outputname, i, j)
                                        if not os.path.exists(temp_img_path):
                                            continue

                                        pic_fole_head = Image.open(temp_img_path)
                                        toImage.paste(pic_fole_head, box=(j * 720, i * 1280))

                                    toImage.save('%s.jpg' % (outputname))

                            for i in range(row):
                                for j in range(line):
                                    temp_img_path = '%s_img_%s_%s.jpg' %(outputname, i, j)
                                    if not os.path.exists(temp_img_path):
                                        continue
                                    os.remove(temp_img_path)
                    except Exception as result:
                        print('error %s' % result)
    return


types = ['.mp4', '.avi', '.wmv', '.mkv', '.flv',
         '.ts', '.mov', '.m4v', '.MOV', '.MP4', '.MKV']
for type in types:
    make_thumb()


