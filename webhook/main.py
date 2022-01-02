from services import Services

def webhook (request):  
    req = request.get_json(force=True) 
    detect_intent = req["queryResult"]["intent"]["displayName"] 
    if 'fulfillment_text' in req:
        res = req.fulfillment_text
    else:
        res = getattr(Services,detect_intent)(req['queryResult'])
    return {'fulfillmentText': res} 