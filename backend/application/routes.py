from application import app
from .devices import *
from .services import Services
from flask import request
devices = {"tv_bedroom":Tv('192.168.0.133', 'bedroom')}

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True) 
    intent = req["queryResult"]["intent"]["displayName"] 
    if 'fulfillment_text' in req:
        res = req.fulfillment_text
    else:
        if intent == 'consult_weather':
            res = Services.consult_weather(req['queryResult']['parameters'])
        if intent =='google_search':
            res = Services.google_search(req['queryResult']['queryText'])
        if intent == 'turn_off':
            getattr(devices['tv_bedrom'],intent)()

    if not res:
        res = 'ok'
    return {'fulfillmentText': res} 
