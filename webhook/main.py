
import logging 
from services import Services

def webhook (request):  
    req = request.get_json(force=True) 
    logging.info ('Request:' + str (req)) 
    detect_intent = req ["queryResult"] ["intent"] ["displayName"] 
    logging.info ('Intent Detected:' + str (detect_intent)) 
    if 'fulfillment_text' in req:
        res = req.fulfillment_text
    else:
        res = getattr(Services,detect_intent)(req['queryResult']['parameters'])
    return {'fulfillmentText': res} 

def welcome (req):
    logging.info(req['queryResult']['parameters']) 
    return 'welcome intent'