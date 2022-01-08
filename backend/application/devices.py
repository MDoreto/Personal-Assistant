from pywebostv.discovery import *
from pywebostv.connection import *
from pywebostv.controls import *
from .timeout import timeout
from .mqtt import send_mqtt
import os
from time import sleep


def check_awaked(ip):
    response = os.system("ping -c 1 -w 1 " + ip + " >/dev/null")
    if response == 0:
        return True
    else:
        return False

class Device:
    def __init__(self, ip):
        self.ip = ip
    @property
    def awaked(self):
        return check_awaked(self.ip)

class Tv(Device):
    _client = None
    @property
    def system(self):
        return SystemControl(self.client)

    @property
    def media(self):
        return MediaControl(self.client)

    @property
    def app(self):
        return ApplicationControl(self.client)

    @property
    def inp(self):
        return InputControl(self.client)

    @property
    def source(self):
        return SourceControl(self.client)

    @property
    def control(self):
        return TvControl(self.client)

    @property
    def client(self):
        if not self.awaked:
            self.switch()
            sleep(2)
        if not self._client:
            client = WebOSClient(self.ip)
            client.connect()
            store = {'client_key': 'a32d4a9287aa406c1f7a1b53c80cea3f'}
            for status in client.register(store):
                if status == WebOSClient.PROMPTED:
                    print("Please accept the connect on the TV!")
                elif status == WebOSClient.REGISTERED:
                    print("Registration successful!")
            self._client =client
            return client

        return self._client
    def __open_app(self,name):
        apps = self.app.list_apps()
        app = [x for x in apps if name in x["title"].lower()][0]
        self.app.launch(app)
    def switch(self):
        send_mqtt('t')
    def connect_to(self, device):
        device_name = device.__qualname__.split('.')[0]
        if device_name == 'Desktop':
            sources = self.source.list_sources()
            self.source.set_source(
                next((x for x in sources if x.label == 'PC'), None))
        if device_name == 'SoundBox':
            outputs = self.media.list_audio_output_sources()
            self.media.set_audio_output(
                next((x for x in outputs if x.data == 'bt_soundbar'), None))

    def volume_down(self):
        self.media.set_volume(self.media.get_volume()['volume'] -10)
    def volume_up(self):
        self.media.set_volume(self.media.get_volume()['volume'] +10)
    def search(self,title):
        if title in ['netflix', 'disney','amazon']:
            self.__open_app(title)
        else:
            inp = InputControl(self.client)
            send_mqtt('s')
            sleep(1)
            self.inp.type(title)
            inp.connect_input()
            for i in range (6):
                inp.right()
            inp.ok() 
            sleep(7)
            inp.ok()
            sleep(20)
            inp.ok()
            inp.disconnect_input()

class Desktop(Device):
    def turn_off():
        print("a")
    def turn_on():
        print("a")

class Light:
    def switch(self):
        send_mqtt('a')

class SoundBox:
    def switch(self):
        send_mqtt('c')
    def connect_to(self, device):
        device_name = device.__qualname__.split('.')[0]
        if device_name == 'Tv':
            send_mqtt('b')
        else:
            send_mqtt('l')
    def volume_up(self):
        send_mqtt('+')
    def volume_down(self):
        send_mqtt('-')