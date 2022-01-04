from os import environ 
from pathlib import Path

class Config(object):
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = 'America/Sao_Paulo'

    MQTT_BROKER_URL = '192.168.0.173'

    
