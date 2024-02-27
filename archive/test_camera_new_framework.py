import queue
import cv2
import time
import os
from sic_framework.core.message_python2 import CompressedImageMessage
from sic_framework.devices import Nao
from sic_framework.devices.common_naoqi.naoqi_camera import NaoqiCameraConf
from sic_framework.devices.common_naoqi.naoqi_text_to_speech import NaoqiTextToSpeechRequest


imgs = queue.Queue()


def on_image(image_message: CompressedImageMessage):
    # we could use cv2.imshow here, but that does not work on Mac OSX
    imgs.put(image_message.image)

# Create camera configuration using vflip to flip the image vertically
#conf = NaoqiCameraConf(res_id=2, fps=30, hflip=1, brightness=100000) # You can also adjust the brightness, contrast, sharpness, etc. See "NaoqiCameraConf" for more
#conf = NaoqiCameraConf(res_id=2, fps=30, hflip=1, brightness=100000) # You can also adjust the brightness, contrast, sharpness, etc. See "NaoqiCameraConf" for more

#nao = Nao(ip='10.0.0.180', top_camera_conf=conf)
ip = '10.0.0.180'
ip = '10.15.3.144'
nao = Nao(ip=ip, top_camera_conf=NaoqiCameraConf(res_id=2, fps=30, hflip=1, vflip=1))
nao.top_camera.register_callback(on_image)

a=[]
a4k=[]
i=0
#connect.say('please look at my head camera')
nao.tts.request(NaoqiTextToSpeechRequest('please look at my head camera'))

while True:
    #connect.adjust_head(-0.2, 0.0)
    # i=i+1
    # s=time.time() 
    img = imgs.get()
    a.append(img)
    #img4k =  video_capture2.read()[1]
    #a4k.append(img4k)
    cv2.imshow('pepper stream', img)
    if len(a)==100:
        nao.tts.request(NaoqiTextToSpeechRequest('please look at my eyes '))
    elif len(a)==200:
        nao.tts.request(NaoqiTextToSpeechRequest('please look at my tablet'))

    elif len(a)==300:
        nao.tts.request(NaoqiTextToSpeechRequest('please look at my left arm '))
    elif len(a)==400:
        nao.tts.request(NaoqiTextToSpeechRequest('please look at my right arm '))
    elif len(a)==500:
        nao.tts.request(NaoqiTextToSpeechRequest('the part ended, please take off your glasses'))

   
'''
os.makedirs('./test/', exist_ok=True)
print("Recording now:")

time.sleep(1)
a = {}
for x in range(30):
    img = imgs.get()
    #cv2.imshow('', img[..., ::-1])  # cv2 is BGR instead of RGB
    a[x] = {'ID':x,'datetime':time.time(),'image':img[..., ::-1]}
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break   
cv2.destroyAllWindows()
print('finished the 90 iterations')

# Save all images to the disk.
for img in a:
    print(img)
    print(a[img])
    print(a[img]['ID'])
    cv2.imwrite(f"{a[img]['ID']:05}.jpg", a[img]['image'])
print("finished saving all images to disk")

# Record the video
height, width, _ = a[0]['image'].shape
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_video.avi', fourcc, 30, (width, height))
for img in a:
    out.write(a[img]['image'])
out.release()
print("finished making video")
print('fin')
'''