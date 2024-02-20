import cv2
import numpy as np
import socket

class PepperCamera:
    def __init__(self, ip='10.0.0.180', port=12345, camera=4):
        self.ip = ip
        self.port = port
        self.camera = camera
        self.socket = socket.socket()
        try:
            self.socket.connect((self.ip, self.port))
            print("Successfully connected with {}:{}".format(self.ip, self.port))
        except Exception as e:
            print("Failed to connect with {}:{}. Error: {}".format(self.ip, self.port, str(e)))
            exit(1)
        
        # Set camera resolution based on the selected camera
        self.width, self.height = self.get_resolution(camera)
        self.size = self.width * self.height * 3  # Assuming RGB format

    def get_resolution(self, camera):
        resolutions = {
            1: (1280, 360),
            2: (2560, 720),
            3: (320, 240),
            4: (640, 480)
        }
        return resolutions.get(camera, (640, 480))  # Default to (640, 480)

    def get_image(self):
        try:
            self.socket.send(b'getImg')
            pepper_img = b""
            while len(pepper_img) < self.size:
                pepper_img += self.socket.recv(self.size - len(pepper_img))
        except Exception as e:
            print("Error receiving image:", str(e))
            return None
        
        return pepper_img

    def close(self):
        self.socket.close()

if __name__ == '__main__':
    pepper_camera = PepperCamera()

    while True:
        try:
            img_data = pepper_camera.get_image()
            if img_data is not None:
                # Convert the received bytes to a numpy array
                img_array = np.frombuffer(img_data, dtype=np.uint8)
                # Check the dimensions of the received image data
                if len(img_array) != pepper_camera.size:
                    print("Received image data size does not match expected size")
                    continue
                # Reshape the array to the correct resolution
                img_rgb = img_array.reshape((pepper_camera.height, pepper_camera.width, 3))
                # Display the image
                cv2.imshow('Pepper Camera', img_rgb)
            else:
                print("Failed to receive image.")
                break
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        except Exception as e:
            print("An error occurred:", str(e))
            break

    pepper_camera.close()
    cv2.destroyAllWindows()


#########################
''' #Three times next to each other in grayscale

import cv2
import numpy as np
import socket

class PepperCamera:
    def __init__(self, ip='10.0.0.180', port=12345, camera=4):
        self.ip = ip
        self.port = port
        self.camera = camera
        self.socket = socket.socket()
        try:
            self.socket.connect((self.ip, self.port))
            print("Successfully connected with {}:{}".format(self.ip, self.port))
        except Exception as e:
            print("Failed to connect with {}:{}. Error: {}".format(self.ip, self.port, str(e)))
            exit(1)
        
        # Set camera resolution based on the selected camera
        self.width, self.height = self.get_resolution(camera)
        self.size = self.width * self.height * 3  # Assuming RGB format

    def get_resolution(self, camera):
        resolutions = {
            1: (1280, 360),
            2: (2560, 720),
            3: (320, 240),
            4: (640, 480)
        }
        return resolutions.get(camera, (640, 480))  # Default to (640, 480)

    def get_image(self):
        try:
            self.socket.send(b'getImg')
            pepper_img = b""
            while len(pepper_img) < self.size:
                pepper_img += self.socket.recv(self.size - len(pepper_img))
        except Exception as e:
            print("Error receiving image:", str(e))
            return None
        
        return pepper_img

    def close(self):
        self.socket.close()

if __name__ == '__main__':
    pepper_camera = PepperCamera()

    while True:
        img_data = pepper_camera.get_image()
        if img_data is not None:
            # Convert the received bytes to a numpy array
            img_array = np.frombuffer(img_data, dtype=np.uint8)
            # Check the dimensions of the received image data
            if len(img_array) != pepper_camera.size:
                print("Received image data size does not match expected size")
                continue
            # Reshape the array to the correct resolution
            img = img_array.reshape((pepper_camera.height, pepper_camera.width, 3))
            # Display the image
            cv2.imshow('Pepper Camera', img)
        else:
            print("Failed to receive image.")
            break
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    pepper_camera.close()
    cv2.destroyAllWindows()
'''