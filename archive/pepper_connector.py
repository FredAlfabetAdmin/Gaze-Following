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


    # def get_img(self):
    #     """
    #     Send signal to pepper to recieve image data, and convert to image data
    #     """
    #     self.s.send(b'getImg')
    #     pepper_img = b""
    #
    #     l = self.s.recv(self.size - len(pepper_img))
    #     while len(pepper_img) < self.size:
    #         pepper_img += l
    #         l = self.s.recv(self.size - len(pepper_img))
    #
    #     im = Image.frombytes("RGB", (self.width, self.height), pepper_img)
    #     cv_image = cv2.cvtColor(np.asarray(im, dtype=np.uint8), cv2.COLOR_BGRA2RGB)
    #
    #     return cv_image[:, :, ::-1]
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
    connect = socket_connection(ip='10.0.0.165', port=12345, camera=4)
    
    # for i in range(1,10):
    #     connect.adjust_head(0.3, 0.01*i)
    #     time.sleep(0.5)
    #     print(i)
    time.sleep(0.5)   
    connect.adjust_head(-0.3, 0)
    time.sleep(0.5) #why I need this ,maybe because of thread protocal,look at server.py or ask people
    
    # while True:
    #     img = connect.get_img()
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
       
    #     cv2.imshow('pepper stream', img)
        
    #     # filename = '/Users/chenglinlin/Desktop/get_img11.png'
    #     # cv2.imwrite(filename, img)
        
    #     cv2.waitKey(1)
        
    a=[]
    i=0
    while True:
        #connect.adjust_head(-0.2, 0.0)
        # i=i+1
        # s=time.time() 
        img =  connect.get_img()
        a.append(img)
        cv2.imshow('pepper stream', img)
       # connect.say('right')
        time.sleep(0.5) 
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


outputpath='/Users/chenglinlin/Documents/gaze following/pitch calibration/'

for n in range(len(a)): 
    #cv2.imshow('pepper stream', a[n])
    cv2.imwrite(f'/Users/chenglinlin/Documents/gaze following/pitch calibration/picture3/{n:05}.jpg',a[n])

file=outputpath
video=file+'testboy3.mp4'
fName = file+'picture3/*.jpg' 
import ffmpeg

(
    ffmpeg
    .input(fName, pattern_type='glob', framerate=5)
    .output(video)
    .run()
)




#the height of pepper is 115.5

#connect Pepper
# connect to VU-ResearchDevice-Net wifi
# in terminal: ssh nao@10.15.3.176 (password: pepper/nao)
# cd stereo_depth && python server.py --cam_id 0 --res_id 1 / python server.py --cam_id 0 --res_id 2 --send_port 12343



# upload documents to server:
#  : mkdir new
#  : scp  /Users/chenglinlin/Documents/code/Socket_Connection/server.py nao@10.15.3.226:~/naoqi/
#  : nano server.py
# revise it
# press ctrl&x to save then rename it

#open local jupyter to run gaze360(here Detectron2 have been installed in my own computer )
# anaconda ->environment choose 'cll'-> open jupyter nootbook

#change jupyter kernel to 'cll'or'tf'(differrent env in anaconda)tensorflow                    2.0.0


# res3  5min  3/s  
# res2 5min   9/s


#cd /Users/chenglinlin/Documents/calibration/CalibrationGame_local-master
# python Calibration5.py 
