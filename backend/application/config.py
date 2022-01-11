from os import environ 

class Config(object):
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = 'America/Sao_Paulo'

    MQTT_BROKER_URL = '192.168.0.173'

    SPOTIPY_CLIENT_ID = environ.get('SPOTIPY_CLIENT_ID')
    SPOTIPY_CLIENT_SECRET = environ.get('SPOTIPY_CLIENT_SECRET')
