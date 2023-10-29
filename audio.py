# streamlit_audio_recorder by stefanrmmr (rs. analytics) - version January 2023

import streamlit as st
from st_audio_rec import st_audiorec

from pydub import AudioSegment

import sst, tts
from pygame import mixer 
import wave
import base64

# DESIGN implement changes to the standard streamlit UI/UX
# --> optional, not relevant for the functionality of the component!
st.set_page_config(page_title="streamlit_audio_recorder")
# Design move app further up and remove top padding
st.markdown('''<style>.css-1egvi7u {margin-top: -3rem;}</style>''',
            unsafe_allow_html=True)
# Design change st.Audio to fixed height of 45 pixels
st.markdown('''<style>.stAudio {height: 45px;}</style>''',
            unsafe_allow_html=True)
# Design change hyperlink href link color
st.markdown('''<style>.css-v37k9u a {color: #ff4c4b;}</style>''',
            unsafe_allow_html=True)  # darkmode
st.markdown('''<style>.css-nlntq9 a {color: #ff4c4b;}</style>''',
            unsafe_allow_html=True)  # lightmode

    

def audiorec_demo_app():
    wav_audio_data, filename = st_audiorec() # tadaaaa! yes, that's it! :D
    print(filename)
    st.write(filename)
    mytext = 'default'
    if wav_audio_data is not None:

        wav_file = AudioSegment.from_wav(filename)
        wav_file.set_frame_rate(48000)
        wav_file.set_channels(2)
        wav_file.export('sency.wav', format='wav')
        mytext = str(sst.recognize('sency.wav'))


    else:
        mytext='default'
        
    return mytext
