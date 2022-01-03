from application import app
from .devices import *
from .services import Services
from flask import request
from flask_apscheduler import APScheduler
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
cred = credentials.Certificate('jarvis-sqri-db7648fb066e.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://jarvis-sqri-default-rtdb.firebaseio.com'
})
ref = db.reference('/Devices')


devices = {"tv_bedroom":Tv('192.168.0.133', 'bedroom')}

@scheduler.task('interval', id='check_devices', seconds=60)
def check_devices():
    ref.set({'tv_bedroom':devices['tv_bedroom'].awaked,'computer':False})


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
    return 'TESTE'


