import qrcode

class QrMake():

    def __init__(self):
        pass
    def make(self,ip,port):
        msg = str(ip) + "@@@" + str(port)
        img = qrcode.make(msg)
        img.save('qr.png')
