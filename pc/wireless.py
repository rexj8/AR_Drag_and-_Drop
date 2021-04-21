import socket
import time
from image_processing import ImageProcessing
from kivymd.toast import toast
class WirelessConnection():

    def __init__(self):
        pass
    def ipfinder(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    def client(self,ip,port):
        print('ok')
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.s.connect((ip, int(port)))

            toast('connected')

        except:
            toast('not connected')
            self.s.close()
            return 0
        time.sleep(0.2)
        self.filegenerator()

    def filegenerator(self):


        with open('new.png', 'wb') as f:
            l = self.s.recv(99216)

            while len(l)!=0:
                f.write(l)
                l = self.s.recv(99216)
            time.sleep(0.2)
            obj = ImageProcessing()
            obj.removeBackGroundWithApi()