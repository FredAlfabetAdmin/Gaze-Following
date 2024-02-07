#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 11:10:38 2023

@author: chenglinlin
"""
import cv2
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
# video_capture1 = cv2.VideoCapture(0)
print("here")
video_capture2 = cv2.VideoCapture(1) # 0 for logitech, 1 for built in
print(type(video_capture2))
print("hi")
video_capture2.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
width = 3840#1000#3840
height = 2160#500#2160
print("haaa")
video_capture2.set(cv2.CAP_PROP_FRAME_WIDTH, width)
print("hoooo")
video_capture2.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
print("hiiiii")

# while True:
#     img = video_capture2.read()[1]
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
   
#     cv2.imshow('pepper stream', img)
    
#     # filename = '/Users/chenglinlin/Desktop/get_img11.png'
#     # cv2.imwrite(filename, img)
    
#     cv2.waitKey(1)

# cv2.destroyAllWindows()

    
a=[]

i=0
while True:
    #connect.adjust_head(-0.2, 0.0)
    # i=i+1
    # s=time.time() 
    img =  video_capture2.read()[1]
    a.append(img)
    cv2.imshow('pepper stream', img)
    print(i)
    i=i+1
    # c=s-time.time()
    # ci=c+ci
    # print(s-time.time())
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #cv2.imshow('pepper stream', img)
    cv2.waitKey(1)

cv2.destroyAllWindows()

for n in range(len(a)): 
    #cv2.imshow('pepper stream', a[n])
    cv2.imwrite(f'/Users/chenglinlin/ownCloud/BETA_AI_Gaze_Estimation_in_Human-Robot_Interaction (Projectfolder)/processed_data/simple_calibration/4k_exp_setting2/{n:05}.jpg',a[n])



# import pandas as pd
# df = pd.DataFrame(b)
# filepath='/Users/chenglinlin/Documents/calibration/CalibrationGame_local-master/compare_test25(lin_res2_sameheight)/robotpos/pos2(headstill)/frametime.csv'
# df.to_csv(filepath) 