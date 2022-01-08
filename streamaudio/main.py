from google.cloud import dialogflow_v2beta1 as dialogflow
import pyaudio
import simpleaudio as sa
import os
import time
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'jarvis-sqri-db7648fb066e.json'
# Audio recording parameters
SAMPLE_RATE = 24000
CHUNK_SIZE = int(SAMPLE_RATE / 10)


def grab_intent(projectId, sessionId, languageCode):
    """Start stream from microphone input to dialogflow API"""
   
    session_client = dialogflow.SessionsClient()
    # Audio output stream
    
    final_request_received = False

    def __request_generator():
        input_stream = pyaudio.PyAudio().open(channels=1,
                rate=SAMPLE_RATE, format=pyaudio.paInt16, input=True)
        audio_encoding = dialogflow.AudioEncoding.AUDIO_ENCODING_LINEAR_16
        session_path = session_client.session_path(projectId, sessionId)
        print('Session path: {}\n'.format(session_path))
        
        input_audio_config = dialogflow.InputAudioConfig(audio_encoding=audio_encoding, 
            language_code=languageCode,
            sample_rate_hertz=SAMPLE_RATE)
        speech_config = dialogflow.SynthesizeSpeechConfig(
            voice=dialogflow.VoiceSelectionParams(ssml_gender=dialogflow.SsmlVoiceGender.SSML_VOICE_GENDER_FEMALE))
        output_audio_config = dialogflow.OutputAudioConfig(
            audio_encoding=dialogflow.OutputAudioEncoding.OUTPUT_AUDIO_ENCODING_LINEAR_16,
            sample_rate_hertz=SAMPLE_RATE,
            synthesize_speech_config=speech_config)
        query_input = dialogflow.QueryInput(audio_config=input_audio_config)

        # The first request contains the configuration.
        yield dialogflow.StreamingDetectIntentRequest(
            session=session_path, query_input=query_input, output_audio_config=output_audio_config)

        while True:
            if final_request_received:
                print("received final request")
                input_stream.close()
                print("closed stream")
                yield
            if input_stream.is_active():
                content = input_stream.read(CHUNK_SIZE, exception_on_overflow = False)
                yield dialogflow.StreamingDetectIntentRequest(input_audio=content)
        



    while True:
        print('=' * 20)
        try:
            requests = __request_generator()
            responses = session_client.streaming_detect_intent(requests =iter(requests))

            for response in responses:
                if response.recognition_result.is_final:
                    text = response.recognition_result.transcript.lower()
                    print(f'Intermediate transcription result: {text}')
                    if 'jarvis' in text:
                        text = text.replace('jarvis','')
                        return detect_intent_texts(projectId, sessionId,text)
                    return False 
        except: 
            return False

def detect_intent_texts(project_id, session_id, text):
    inicio = time.time()
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.TextInput(
            text=text, language_code='pt-BR')
        query_input = dialogflow.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        print(time.time() - inicio)
        return response
        
def play_audio(audio):
    audio_obj = sa.play_buffer(audio, 1, 2, SAMPLE_RATE)
    audio_obj.wait_done()

def main():
    while(True):
        response = grab_intent('jarvis-sqri', 'unique', 'pt-BR')
        if response:
            play_audio(response.output_audio)

if __name__ == "__main__":
    main()