
from kivy.uix.behaviors import DragBehavior
import platform,os

from wireless import WirelessConnection
from kivy.uix.image import Image
import random,threading
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import DragBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import rgba
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from image_processing import ImageProcessing
class ImageButton(ButtonBehavior, Image):
    pass

class MainWindow(BoxLayout):
    container = ObjectProperty(None)
class ShowQr(BoxLayout):
    qr = ObjectProperty(None)

class DragImage(DragBehavior, Image):
    pass
class Qrreader(BoxLayout):
    zbarcam=ObjectProperty(None)
    qroutput=ObjectProperty(None)
class uiApp(MDApp):
    portused={}

    container = None
    def build(self):
        self.screen_manager = ScreenManager()

        self.builderscreen = MainWindow()
        screen = Screen(name='builderscreen')
        screen.add_widget(self.builderscreen)
        self.screen_manager.add_widget(screen)

        uiApp.container = self.builderscreen.container
        self.qrreasderscreen = Qrreader()
        screen = Screen(name='qrreasderscreen')
        screen.add_widget(self.qrreasderscreen)
        self.screen_manager.add_widget(screen)
        print('okk')
        Clock.schedule_interval(self.callback, 2)
        return self.screen_manager
    def callback(self, dt):
        if os.path.isfile('transparent.png'):
            img = DragImage(source="transparent.png")
            uiApp.container.add_widget(img)
            os.remove('transparent.png')
            os.remove('new.png')


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


    def clientthread(self,ip,port):

        obj1 = WirelessConnection()
        obj1.client(ip,port)
    def qrcontinuosreader(self,dt):
        if len(self.qrreasderscreen.qroutput.text)>8 and '@@@' in self.qrreasderscreen.qroutput.text:
            data = str(self.qrreasderscreen.qroutput.text)
            data = data.replace("b'","")
            data = data.replace("'","")
            data = data.split("@@@")
            ip = data[0]
            port = data[1]
            thread = threading.Thread(target=self.clientthread,args=(ip,port))
            thread.start()
            print(ip)

            self.receivescreen_to_mainscreen()
        else:

            Clock.schedule_once(self.qrcontinuosreader, 0.5)




    def mainscreen_to_receivescreen(self):

        self.screen_manager.transition.direction = 'down'
        self.screen_manager.current = 'qrreasderscreen'
        Clock.schedule_once(self.qrcontinuosreader, 0.5)

    def receivescreen_to_mainscreen(self):

        self.screen_manager.transition.direction = 'up'
        self.screen_manager.current = 'builderscreen'
uiApp().run()