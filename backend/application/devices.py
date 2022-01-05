from pywebostv.discovery import *
from pywebostv.connection import *
from pywebostv.controls import *
from .timeout import timeout
import os


def check_awaked(ip):
    response = os.system("ping -c 1 -w 1 " + ip)
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
        client = WebOSClient(self.ip)
        client.connect()
        store = {'client_key': 'a32d4a9287aa406c1f7a1b53c80cea3f'}
        for status in client.register(store):
            if status == WebOSClient.PROMPTED:
                print("Please accept the connect on the TV!")
            elif status == WebOSClient.REGISTERED:
                print("Registration successful!")
        return client
    def turn_off(self):
        self.system.power_off()

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

class Desktop(Device):
    def turn_off():
        print("a")
    def turn_on():
        print("a")

