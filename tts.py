import os
from google.cloud import texttospeech
import json
import streamlit as st
from pygame import mixer 
import base64

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
with open("eduavatar-m-hamza-321734316044.json", "w") as json_file:
    json.dump(google_json, json_file)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="eduavatar-m-hamza-321734316044.json"

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="true">
            <source src="data:audio/wav;base64,{b64}" type="audio/wav">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )


def tts(text, col):

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US")
    # ****** the NAME
    # and the ssml voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code='ar-XA',
        name='ar-XA-Standard-A',
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    # The response's audio_content is binary.
    print('were gonna play something')
    with open('output.wav', 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)
    try:
        with col:
            autoplay_audio('output.wav')
    except:
        autoplay_audio
    return out
        
