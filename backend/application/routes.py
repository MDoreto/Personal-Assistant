from application import app
from .devices import *
from .services import Services
from flask import request
from flask_apscheduler import APScheduler
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

devices = {"tv_bedroom":Tv('192.168.0.133'),
            "desktop_bedroom":Desktop('192.168.0.30'),
            "nodemcu_bedroom":Desktop('192.168.0.217'),
            "light_bedroom": Light(),
            "soundbox_bedroom":SoundBox()}

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
        if intent == 'turn_on':
            temp = devices[req['queryResult']['parameters']['device']]
            if hasattr(temp, intent):
                getattr(temp,intent)()
            else:
                temp.switch()
        if intent == 'turn_off':
            temp = devices[req['queryResult']['parameters']['device']]
            if hasattr(temp, intent):
                getattr(temp,intent)()
            else:
                temp.switch()
        if intent in ['volume_up','volume_down']:
            getattr(devices[req['queryResult']['parameters']['device']],intent)()
            
    return {'fulfillmentText': res} 

@app.route('/api', methods=['POST'])
def api():
    device = request.json['device']
    action = request.json['action']
    getattr(devices[device],action)(request.json['title'])
    return {'message':'command has been executed'}
@app.route('/')
def test():
    devices['tv_bedroom'].search('encanto')
    return 'teste'


