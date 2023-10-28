import os
from google.cloud import speech
import tts
import json


#json_file=json.loads(str(os.environ.get('GOOGLE_JSON')))
#with open("eduavatar-m-hamza-321734316044.json", "w") as outfile:
#    outfile.write(json_file)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="eduavatar-m-hamza-321734316044.json"

def recognize(file) -> speech.RecognizeResponse:
    print('entering')
    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    gcs_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.raw"

    with open(file, "rb") as audio_file:
        content = audio_file.read()
    print('hii')

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
