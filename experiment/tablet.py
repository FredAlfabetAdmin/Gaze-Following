#------------------------------- Preparations: -------------------------------#
# Imports
import time
from sic_framework.devices.common_naoqi.pepper_tablet import UrlMessage
from sic_framework.devices import Pepper

# Variables
pepper = None
arrow_left =  'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/U%2B2190.svg/2560px-U%2B2190.svg.png'
arrow_right = 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/U%2B2192.svg/2560px-U%2B2192.svg.png'
flag_empty = 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/White_flag_of_surrender.svg/2560px-White_flag_of_surrender.svg.png'
vu_logo = 'https://assets.vu.nl/d8b6f1f5-816c-005b-1dc1-e363dd7ce9a5/f421a17a-498d-48e7-bae6-ba6fae122d72/VU_logo_RGB-01.png'

#------------------------------- Functions: -------------------------------#
def set_pepper_tablet(_pepper):
    global pepper
    pepper = _pepper

def show_tablet_left():
    print("Showing left")
    time.sleep(0.5)
    pepper.tablet_display_url.send_message(UrlMessage(arrow_left))
    
def show_tablet_right():
    print("Showing right")
    time.sleep(0.5)
    pepper.tablet_display_url.send_message(UrlMessage(arrow_right))
    
def show_tablet_empty():
    print("showing none")
    pepper.tablet_display_url.send_message(UrlMessage(flag_empty))

def show_tablet_vu_logo():
    print("showing VU logo")
    pepper.tablet_display_url.send_message(UrlMessage(vu_logo))