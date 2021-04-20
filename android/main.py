from datetime import time
import time
from kivy.core.text import LabelBase
import random,threading

from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import DragBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import rgba
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.toast import toast
from wireless import WirelessConnection
from qrmaker import QrMake
class ImageButton(ButtonBehavior, Image):
    pass
class CameraWindow(BoxLayout):
    camera = ObjectProperty(None)

class MainWindow(BoxLayout):
    content = ObjectProperty(None)
class ShowQr(BoxLayout):
    qr = ObjectProperty(None)

class uiApp(MDApp):
    portused={}
    def helptext(self):
        content = ["[color=#96bb7c]1)[/color] first of  connect and phone pc \n with the hotspot of another mobile ",
                   "\n",
                   "[color=#96bb7c]2)[/color] make sure application should be running \n on both pc and mobile",
                   "\n",
                   "[color=#96bb7c]3)[/color] then capture image in phone using the \n given button ",
                   "\n",
                   "[color=#96bb7c]4)[/color] then click on scan qr button on phone",
                   "\n",
                   "[color=#96bb7c]5)[/color] now click on signal botton on pc application \n you will notice camera will started",
                   "\n",
                   "[color=#96bb7c]6)[/color] now show the qr(shown on phone screen) to \n camera runnning on pc",
                   "\n",
                   "[color=#96bb7c]7)[/color] if a pop up of [color=#FF0000]not connected[/color] appeared on \n either of two devices then repeat process \nfrom step 4",
                   "\n",
                   "[color=#96bb7c]8)[/color] if pop up of [color=#32CD32]connected[/color] is shown on either \n os two devices then wait for some time \n your captured image will be shown \n on pc application",
                   "\n",
                   "[color=#96bb7c]9)[/color] if popup of [color=#FF0000]can't show image[/color] appeared on \n pc then repeat process from step 4",
                   "\n",
                   "[color=#96bb7c]10)[/color] if popup donot appeared on \n pc then wait your image \n will get appeared soon",
                   "\n",
                   "[color=#32CD32]Tip :- [/color]you can also drag the image   \n which will appear pc",
                   ]
        k="[color=#9dad7f]"
        for i in content:
            k+=i
        k+="[/color]"
        self.builderscreen.content.text=k
    def build(self):
        self.screen_manager = ScreenManager()

        self.builderscreen = MainWindow()
        screen = Screen(name='builderscreen')
        screen.add_widget(self.builderscreen)
        self.screen_manager.add_widget(screen)
        self.helptext()
        self.camerascreen = CameraWindow()
        screen = Screen(name='camerascreen')
        screen.add_widget(self.camerascreen)
        self.screen_manager.add_widget(screen)

        self.qrscreen = ShowQr()
        screen = Screen(name='qrscreen')
        screen.add_widget(self.qrscreen)
        self.screen_manager.add_widget(screen)

        return self.screen_manager
    def sendImage(self):
        pass
    def capture(self):
        #self.camerascreen.camera.export_to_png("temp.png")
        self.camerascreen.camera.export_to_png("/storage/emulated/0/temp.png")
        toast("Captured")
    def portNumberGenerator(self):
        port = None
        while True:
            port = random.randrange(30000, 35000, 1)
            if port not in uiApp.portused:
                uiApp.portused[port] = True
                break
        return port
    def mainscreen_to_camerascreen(self):
        self.screen_manager.transition.direction = 'right'
        self.screen_manager.current = 'camerascreen'
    def camerascreen_to_mainscreen(self):
        self.screen_manager.transition.direction = 'left'
        self.screen_manager.current = 'builderscreen'
    def mainscreen_to_qrscreen(self):
        try:
            self.qrscreen.qr.reload()
        except:
            print("can't refresh qr")
        obj1 = WirelessConnection()

        ip = obj1.ipfinder()
        port = self.portNumberGenerator()
        obj2 = QrMake()
        obj2.make(ip,port)
        self.screen_manager.transition.direction = 'down'
        self.screen_manager.current = 'qrscreen'
        thread = threading.Thread(target=self.serverthread,args=(ip,port))
        thread.start()

    def serverthread(self,ip,port):
        obj1 = WirelessConnection()
        obj1.server(ip, port)
        self.qrscreen_to_mainscreen()
    def qrscreen_to_mainscreen(self):
        self.screen_manager.transition.direction = 'up'
        self.screen_manager.current = 'builderscreen'

LabelBase.register(name='pacifico',
                   fn_regular='fonts/Pacifico-Regular.ttf')
uiApp().run()