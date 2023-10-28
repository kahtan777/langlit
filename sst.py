import os
from google.cloud import speech
import tts
import json
import streamlit as st


google_json={
    'universe_domain': st.secrets['universe_domain'],
    'client_x509_cert_url': st.secrets['client_x509_cert_url'],
    'auth_provider_x509_cert_url': st.secrets['auth_provider_x509_cert_url'],
    'client_email': st.secrets['client_email'],
    'client_id': st.secrets['client_id'],
    'auth_uri': st.secrets['auth_uri'],
    'token_uri': st.secrets['token_uri'],
    'private_key': st.secrets['private_key'],
    'private_key_id': st.secrets['private_key_id'],
    'project_id': st.secrets['project_id'],
    'type': st.secrets['type']
}
print('before')
with open("eduavatar-m-hamza-321734316044.json", "w") as json_file:
    json.dump(google_json, json_file)
print('after')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="eduavatar-m-hamza-321734316044.json"

def recognize(file) -> speech.RecognizeResponse:
    print('enteringgggggg')
    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    gcs_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.raw"

    with open(file, "rb") as audio_file:
        content = audio_file.read()
    print('hiiiiiiiiiiiiiii')

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code="ar-XA",
        audio_channel_count=2
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    print('response')

    tts.tts('مرحبا كيف حالك؟')

    
    try:
        for result in response.results:
            print(f"Transcript: {result.alternatives[0].transcript}")
        return result.alternatives[0].transcript
    except:
        return ''
