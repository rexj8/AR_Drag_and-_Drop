import socket
import time

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


    def server(self,ip,port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(ip)
        # self.sendscreen.ip.text, int(self.sendscreen.port.text)
        try:
            s.bind((ip, int(port)))

        except:
            toast('something is incorrect with your data')
            s.close()

            return 0
        s.listen(4)


        toast('working')

        print('oktry')
        self.clientsocket, address = s.accept()
        while len(address)==0:
            self.clientsocket, address = s.accept()
            print('ok')

        toast(f"Connection from {address} has been established.")

        time.sleep(0.2)
        self.filebreaker()

    def filebreaker(self):
        with open('/storage/emulated/0/temp.png', 'rb') as f:

            l = f.read(99216)

            while len(l)!=0:
                self.clientsocket.send(l)
                l = f.read(99216)


