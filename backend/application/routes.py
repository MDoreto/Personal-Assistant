from application import app
from .devices import *
from .services import *
from .spotify import sp
import application.spotify as spotify
from flask import request
from flask_apscheduler import APScheduler
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

devices = {"tv_bedroom":Tv('192.168.0.133'),
            "desktop_bedroom":Desktop('192.168.0.30'),
            "nodemcu_bedroom":Desktop('192.168.0.217'),
            "light_bedroom": Light(),
            "soundbox_bedroom":SoundBox(),
            "spotify":spotify}

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
    parameters = req['queryResult']['parameters']
    res = 'ok'
    if 'fulfillment_text' in req:
        res = req.fulfillment_text
    else:
        if intent == 'consult_weather':
            res = consult_weather(parameters)
        if intent =='google_search':
            res = google_search(req['queryResult']['queryText'])
        if intent in  ['turn_on', 'turn_off']:
            getattr(devices[parameters['device']],'switch')()
        if intent in ['volume_up','volume_down','next_music','prev_music']:
            getattr(devices[parameters['device']],intent)()
        if intent=='stop_music':
            spotify.stop_music()
        if intent=='play_music':
            return get_response(**spotify.play_music())
        if intent == 'get_music_name':
            return get_response(**spotify.search_music(parameters['any']))
        if intent == 'get_device':
            parameters = next((x for x in req['queryResult']['outputContexts'] if 'expecting_device' in x['name']), None)['parameters']
            if parameters['intent'] =='search_music':
                getattr(devices[parameters['device']],'search')('spotify')
                return get_response(**spotify.search_music(parameters['any']))
            if parameters['intent'] =='play_music':
                getattr(devices[parameters['device']],'search')('spotify')
                return get_response(**spotify.play_music())

    response = {'fulfillmentText': res} 
    return response

@app.route('/api', methods=['POST'])
def api():
    device = request.json['device']
    action = request.json['action']
    getattr(devices[device],action)()
    return {'message':'command has been executed'}
@app.route('/')
def test():
    print(sp.devices())
    return 'teste'

def get_response(text='ok',context='', parameters={}):
    response = {'fulfillmentText': text} 
    if context:
        response['contextOut'] = {'name':"projects/jarvis-sqri/agent/sessions/unique/contexts/" + context , "lifespan":1, "parameters":parameters} 
    return response
