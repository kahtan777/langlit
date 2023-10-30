from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import os
import audio
import streamlit as st
from streamlit_chat import message
from utils import *
import tts
import wave
import contextlib
import streamlit.components.v1 as components
import time




keyy=st.secrets["openAI_key"]
st.set_page_config(layout="wide")
left_column, right_column = st.columns([5,5])

with left_column:
    video_html = """
    <style>
    .video-container {
        width: 30%;
        height: auto;
        overflow: hidden;
        border-radius: 0;
        position: fixed;
        top: 5%;
        left: 3%;
        z-index: 999; /* Ensure the video appears above other content */
    }

    @media (max-width: 768px) {
        .video-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 95%;
        }
    }

    video {
        width: 100%;
        height: auto;
    }

    .content {
        background: rgba(0, 0, 0, 0.5);
        color: #f1f1f1;
        width: 100%;
        padding: 45%;
    }
    </style>
    <div class="video-container floating">
        <video autoplay muted loop id="myVideo">
            <source src="https://futurelaby.com/avatar/2023-10-28%2014-19-34.mp4">
            Your browser does not support HTML5 video.
        </video>
    </div>
    
    <script>
        const video = document.getElementById('myVideo');
    
        video.addEventListener('loadedmetadata', () => {
            if (video.requestPictureInPicture) {
                video.requestPictureInPicture();
            }
        });
    </script>
    """

    st.markdown(video_html, unsafe_allow_html=True)




with right_column:
    st.subheader("Hey little cupcakes, today am gonna be your teacher :)")
    if 'responses' not in st.session_state:
        st.session_state['responses'] = ["مرحبا، انا مريم رح كون انستكون ليوم"]
    
    if 'requests' not in st.session_state:
        st.session_state['requests'] = []
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=keyy)
    
    if 'buffer_memory' not in st.session_state:
                st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3,return_messages=True)
    
    
    system_msg_template = SystemMessagePromptTemplate.from_template(template="""Answer the question as truthfully as possible using the provided context in Arabic only, 
    and if the answer is not contained within the text below, say 'I don't know', but if its a greeting you have to greet back, and be friendly female teacher,and your name is mariam, act as teacher your name is mariam""")
    
    
    human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")
    
    prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])
    
    conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)
    
    
    
    
   
    # container for chat history
    with right_column:
        response_container = st.container()
    # container for text box
    with right_column: 
        textcontainer = st.container()
    
    with right_column:
        mytext = audio.audiorec_demo_app(right_column)
    
    def change_my_text_back():
        mytext='default'
        
    
    with textcontainer:
        if mytext == 'default':
            query = st.text_input("Question: ", key="input", on_change=change_my_text_back)
        else:
            query = st.text_input("Question: ", key="input", value=mytext, on_change=change_my_text_back)
        if query:
            with st.spinner("typing..."):
                #conversation_string = get_conversation_string()
                #st.code(conversation_string)
                #refined_query = query_refiner(conversation_string, query)
                #st.subheader("Refined Query:")
                #st.write(refined_query)
                context = find_match(query)#refined_query
                # print(context)  
                response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query}")
                filename_ = tts.tts(response, left_column)
                with wave.open(filename_) as mywav:
                    duration_seconds = mywav.getnframes() / mywav.getframerate()
                    change_avatar(duration_seconds)
                
            st.session_state.requests.append(query)
            st.session_state.responses.append(response) 
    with response_container:
        if st.session_state['responses']:
    
            for i in range(len(st.session_state['responses'])):
                message(st.session_state['responses'][i],key=str(i))
                if i < len(st.session_state['requests']):
                    message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')

def play_audio(where):
    return


