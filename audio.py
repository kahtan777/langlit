# streamlit_audio_recorder by stefanrmmr (rs. analytics) - version January 2023

import streamlit as st
from st_audio_rec import st_audiorec

from pydub import AudioSegment

import sst, tts
from pygame import mixer 
import wave
import base64
    

def audiorec_demo_app(col):
    wav_audio_data, filename = st_audiorec() # tadaaaa! yes, that's it! :D
    print(filename)
    mytext = 'default'
    if wav_audio_data is not None:

        wav_file = AudioSegment.from_wav(filename)
        try:
            wav_file.set_frame_rate(48000)
            wav_file.set_channels(2)
            wav_file.export('sency.wav', format='wav')
            mytext = str(sst.recognize('sency.wav', col))
        except:
            mytext= 'default'


    else:
        mytext='default'
        
    return mytext
