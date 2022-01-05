from application import app
from .devices import *
from .services import Services
from flask import request
from flask_apscheduler import APScheduler
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from flask_mqtt import Mqtt

devices = {"tv_bedroom":Tv('192.168.0.133'),
            "desktop_bedroom":Desktop('192.168.0.30'),
            "nodemcu_bedroom":Desktop('192.168.0.217')}

mqtt = Mqtt()
mqtt.init_app(app)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('NodeMcu')
    mqtt.subscribe('Desktop/Status')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print(data)

def send_mqtt(topic, text):
    mqtt.publish(topic, text)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

@scheduler.task('interval', id='check_devices', seconds=5)
def check_devices():
    data ={}
    for att  in devices:
        if hasattr(devices[att],'awaked'):
            data[att] = devices[att].awaked
    ref.set(data)


cred = credentials.Certificate('jarvis-sqri-db7648fb066e.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://jarvis-sqri-default-rtdb.firebaseio.com'
})
ref = db.reference('/Devices')



@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True) 
    intent = req["queryResult"]["intent"]["displayName"] 
    res = 'ok'
    if 'fulfillment_text' in req:
        res = req.fulfillment_text
    else:
        if intent == 'consult_weather':
            res = Services.consult_weather(req['queryResult']['parameters'])
        if intent =='google_search':
            res = Services.google_search(req['queryResult']['queryText'])
        if intent == 'turn_off':
            getattr(devices[req['queryResult']['parameters']['device']],intent)()
    return {'fulfillmentText': res} 
@app.route('/')
def test():
    send_mqtt('NodeMcu', 'TESTE')
    return str(devices['desktop_bedroom'].awaked)


