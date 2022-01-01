import time
import os
from google.cloud import dialogflow_v2beta1 as dialogflow
from flask import Flask, request, send_file
from flask_cors import CORS
import subprocess
app = Flask(__name__)
CORS(app)


def detect_intent_texts(project_id, session_id, text):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.TextInput(
            text=text, language_code='pt-BR')
        query_input = dialogflow.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        return response


def detect_intent_audio(project_id='jarvis-sqri', session_id='unique'):
    """Returns the result of detect intent with an audio file as input.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()

    # Note: hard coding audio_encoding and sample_rate_hertz for simplicity.
    audio_encoding = dialogflow.AudioEncoding.AUDIO_ENCODING_LINEAR_16
    sample_rate_hertz = 16000

    session = session_client.session_path(project_id, session_id)

    with open('audio.wav', "rb") as audio_file:
        input_audio = audio_file.read()

    audio_config = dialogflow.InputAudioConfig(
        audio_encoding=audio_encoding,
        language_code='pt-BR',
        sample_rate_hertz=sample_rate_hertz,
    )
    query_input = dialogflow.QueryInput(audio_config=audio_config)

    request = dialogflow.DetectIntentRequest(
        session=session, query_input=query_input, input_audio=input_audio,
    )
    response = session_client.detect_intent(request=request)
    return response


@app.route('/message', methods=['POST'])
def send_message():
    message = request.json['text']

    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    res = detect_intent_texts(project_id, "unique", message)

    return res.__class__.to_json(res)


@app.route('/audio', methods=['POST'])
def send_audio():
    file = request.files['audio']
    file.save("message.webm")
    os.system('ffmpeg -i message.webm -c copy correct.webm')
    os.system(f'ffmpeg -i correct.webm -vn -ar 16000 -ac 1 -ab 192 -f wav audio.wav')
    res = detect_intent_audio()
    os.remove('correct.webm')
    os.remove('audio.wav')
    with open("output.wav", "wb") as out:
        out.write(res.output_audio)
    return res.__class__.to_json(res)


@app.route('/audio_file')
def get_audio():
    return send_file('output.wav',
                     mimetype='audio/wav',
                     as_attachment=True,
                     attachment_filename='sound.wav')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
