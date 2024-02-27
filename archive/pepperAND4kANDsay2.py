#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 11:22:56 2024

@author: chenglinlin
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 13:13:07 2024

@author: chenglinlin
"""

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
video_capture2 = cv2.VideoCapture(0) # 0 for logitech, 1 for built in

video_capture2.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
width = 1000#3840
height = 500#2160
video_capture2.set(cv2.CAP_PROP_FRAME_WIDTH, width)
video_capture2.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


import socket
import cv2
import numpy as np
from PIL import Image
import time

class socket_connection():
    """
    Class for creating socket connection and retrieving images
    """
    def __init__(self, ip, port, camera, **kwargs):
        """
        Init of vars and creating socket connection object.
        Based on user input a different camera can be selected.
        1: Stereo camera 1280*360
        2: Stereo camera 2560*720
        3: Mono camera 320*240
        4: Mono camera 640*480
        """
        # Camera selection
        if camera == 1:
            self.size = 1382400  # RGB
            self.size = 921600  # YUV422
            self.width = 1280
            self.height = 360
            self.cam_id = 3
            self.res_id = 14
        elif camera == 2:
            self.size = 5529600  # RGB
            self.size = 3686400  # YUV422
            self.width = 2560
            self.height = 720
            self.cam_id = 3
            self.res_id = 13
        elif camera == 3:
            self.size = 230400
            self.width = 320
            self.height = 240
            self.cam_id = 0
            self.res_id = 1
        elif camera == 4:
            self.size = 614400
            self.width = 640
            self.height = 480
            self.cam_id = 0
            self.res_id = 2
      
        else:
            print("Invalid camera selected... choose between 1 and 4")

        self.COLOR_ID = 13
        self.ip = ip
        self.port = port

        # Initialize socket socket connection
        self.s = socket.socket()
        try:
            self.s.connect((self.ip, self.port))
            print("Successfully connected with {}:{}".format(self.ip, self.port))
        except:
            print("ERR: Failed to connect with {}:{}".format(self.ip, self.port))
            exit(1)


    def get_img(self):
        #     """
        #     Send signal to pepper to recieve image data, and convert to image data
        #     """
        self.s.send(b'getImg')
        pepper_img = b""

        l = self.s.recv(self.size - len(pepper_img))
        print(self.size,len(pepper_img))
        print('I have not gone into the loop')
        while len(pepper_img) < self.size:
            print("in the loop")
            pepper_img += l
            l = self.s.recv(self.size - len(pepper_img))
            print('len=',len(pepper_img))

        arr = np.frombuffer(pepper_img, dtype=np.uint8)
        y = arr[0::2]
        u = arr[1::4]
        v = arr[3::4]
        yuv = np.ones((len(y)) * 3, dtype=np.uint8)
        yuv[::3] = y
        yuv[1::6] = u
        yuv[2::6] = v
        yuv[4::6] = u
        yuv[5::6] = v
        yuv = np.reshape(yuv, (self.height, self.width, 3))
        image = Image.fromarray(yuv, 'YCbCr').convert('RGB')
        image = np.array(image)
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        return image

    def close_connection(self):
        """
        Close socket connection after finishing
        """
        return self.s.close()

    def say(self, text):
        self.s.sendall(bytes(f"say {text}".encode()))

    def enable_tracking(self):
        self.s.sendall(bytes("track True".encode()))

    def disable_tracking(self):
        self.s.sendall(bytes("track False".encode()))

    def nod(self):
        self.s.sendall(bytes("nod".encode()))

    def adjust_head(self, pitch, yaw):
        self.s.sendall(bytes("head {:0.2f} {:0.2f}".format(pitch, yaw).encode()))

    def idle(self):
        self.s.sendall(bytes("idle".encode()))


if __name__ == '__main__':
    connect = socket_connection(ip='10.0.0.165', port=12348, camera=4)
    
   # for i in range(1,10):
    #     connect.adjust_head(0.3, 0.01*i)
    #     time.sleep(0.5)
    #     print(i)
    time.sleep(0.5)   
    connect.adjust_head(-0.3, 0)
    time.sleep(10) #why I need this ,maybe because of thread protocal,look at server.py or ask people
    

    a=[]
    a4k=[]
    i=0
    connect.say('please look at my head camera')
    while True:
        #connect.adjust_head(-0.2, 0.0)
        # i=i+1
        # s=time.time() 
        # img =  connect.get_img()
        # a.append(img)
        img4k =  video_capture2.read()[1]
        a4k.append(img4k)
        cv2.imshow('pepper stream', img4k)
        if len(a)==100:
            connect.say('please look at my eyes ')
        elif len(a)==200:
            connect.say('please look at my tablet')
  
        elif len(a)==300:
            connect.say('please look at my left arm ')
        elif len(a)==400:
            connect.say('please look at my right arm ')
        elif len(a)==500:
            connect.say('the part ended, please take off your glasses')
            
        elif len(a)==700:
            connect.say('please look at head camera')
  
        elif len(a)==800:
            connect.say('please look at my eyes ')   
        elif len(a)==900:
            connect.say('please look at my tablet')
  
        elif len(a)==1000:
            connect.say('please look at my left arm ')
        elif len(a)==1100:
            connect.say('please look at my right arm ')
        elif len(a)==1200:
            connect.say('calibration finished! thanks very much!')
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
        #cv2.imshow('pepper stream', img)
        cv2.waitKey(1)
    cv2.destroyAllWindows()
   
  
    for n in range(len(a4k)): 
        #cv2.imshow('pepper stream', a[n])
        cv2.imwrite(f'/Users/chenglinlin/Documents/gaze tracking/AOItest/participant2/peppercamera/{n:05}.jpg',a[n])
        cv2.imwrite(f'/Users/chenglinlin/Documents/gaze tracking/AOItest/participant2/4kcamera/{n:05}.jpg',a4k[n])

    for n in range(2019,2819):
            #cv2.imshow('pepper stream', a[n])
        cv2.imwrite(f'/Users/chenglinlin/Documents/gaze tracking/AOItest/cammeraNimat/peppercamera/{n-2019:05}.jpg',a[n])
        cv2.imwrite(f'/Users/chenglinlin/Documents/gaze tracking/AOItest/cammeraNimat/4kcamera/{n-2019:05}.jpg',a4k[n])

# participant2 girl 164

# import pandas as pd
# df = pd.DataFrame(b)
# filepath='/Users/chenglinlin/Documents/calibration/CalibrationGame_local-master/compare_test25(lin_res2_sameheight)/robotpos/pos2(headstill)/frametime.csv'
# df.to_csv(filepath) 