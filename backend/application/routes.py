from application import app
from flask import request
from google.cloud import dialogflow_v2beta1 as dialogflow
import os

def detect_intent_texts(project_id, session_id, text):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.TextInput(
            text=text, language_code='pt-BR')
        query_input = dialogflow.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        return response.query_result


@app.route('/dialogflow', methods=['POST'])
def send_message():
    message = request.json['text']
    print(message)
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    res = detect_intent_texts(project_id, "unique", message)
    return res.fulfillment_text
