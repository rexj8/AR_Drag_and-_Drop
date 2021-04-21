
import cv2
import numpy as np
from kivymd.toast import toast
import requests


class ImageProcessing():


    def __init__(self):
        pass

    def removeBackGroundWithApi(self):


        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': open('new.png', 'rb')},
            data={'size': 'auto'},
            headers={'X-Api-Key': 'Fmga67bcMetjP14dwVZU9vwe'},
        )
        if response.status_code == requests.codes.ok:
            with open('transparent.png', 'wb') as out:
                out.write(response.content)
        else:
            print("Error:", response.status_code, response.text)
            toast("can't show image")



