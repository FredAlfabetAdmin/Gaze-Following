
import queue
import cv2
from sic_framework.core.message_python2 import CompressedImageMessage
from sic_framework.devices import Nao, Pepper
from sic_framework.devices.common_naoqi.naoqi_camera import NaoqiCameraConf

imgs = queue.Queue()


def on_image(image_message: CompressedImageMessage):
    # we could use cv2.imshow here, but that does not work on Mac OSX
    imgs.put(image_message.image)

# Create camera configuration using vflip to flip the image vertically
conf = NaoqiCameraConf(vflip=1, saturation=128) # You can also adjust the brightness, contrast, sharpness, etc. See "NaoqiCameraConf" for more
#conf = NaoqiCameraConf(naoqi_ip='127.0.0.1', port=9559, cam_id=0, res_id=2, fps=30, brightness=55, contrast=32, saturation=128, hue=0, gain=32, hflip=0, vflip=1, auto_exposition=1, auto_white_bal=1, auto_exp_algo=1, sharpness=0, back_light_comp=1)
conf = NaoqiCameraConf(naoqi_ip='127.0.0.1',
                        port=9559,
                          cam_id=0,
                            res_id=2,
                              fps=30,
                                brightness=0,
                                  contrast=16,
                                    saturation=64,
                                      hue=0,
                                        gain=16,
                                          hflip=0,
                                            vflip=1,
                                              auto_exposition=1,
                                                auto_white_bal=1,
                                                  auto_exp_algo=1,
                                                    sharpness=0,
                                                      back_light_comp=1)

nao = Pepper(ip="10.0.0.180", top_camera_conf=conf)
nao.top_camera.register_callback(on_image)

while True:
    img = imgs.get()
    #cv2.imshow('', img[..., ::-1])  # cv2 is BGR instead of RGB
    cv2.imshow('', img)  # cv2 is BGR instead of RGB
    
    #cv2.imwrite(f'output_{x}.png', img[..., ::-1])
    cv2.waitKey(1)
