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

keyy=st.secrets["openAI_key"]

st.set_page_config(layout="wide")

left_column, right_column = st.columns([7,3])

with left_column:
    video_html = """
    <style>
    .video-container {
        width: 60%; /* Adjust the width to your desired size */
        height: auto;
        overflow: hidden; /* Add overflow hidden to clip round edges */
        border-radius: 0; /* Apply border-radius to make it round-edged */
        position: fixed; /* Fixed position to keep it in the top left corner for desktop */
        top: 5%;
        left: 3%;
    }

    @media (max-width: 768px) {
        .video-container {
            position: fixed; /* Fixed position for mobile */
            top: 0;
            left: 0;
            width: 100%; /* Full width for mobile */
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
        padding: 60px;
    }
    </style>    
    <div class="video-container">
    <video autoplay muted loop id="myVideo">
        <source src="https://futurelaby.com/avatar/2023-10-28%2014-19-34.mp4">
        Your browser does not support HTML5 video.
    </video>
    </div>
    """
    st.markdown(video_html, unsafe_allow_html=True)



st.markdown("""
<style>
@media (max-width: 768px) {
    .video-container {
        width: 100%; /* Adjust the width to fill the screen width */
        top: 30%; /* Move to the top */
        left: 0; /* Move to the left */
    }

    .content {
        width: 100%; /* Adjust the width to fill the screen width */
        padding: 30px; /* Add some padding to separate from the video */
    }

    .textcontainer {
        width: 100%; /* Adjust the width to fill the screen width */
        padding: 30px; /* Add some padding to separate from the video */
    }
}
</style>
""", unsafe_allow_html=True)

with right_column:
    if 'responses' not in st.session_state:
        st.session_state['responses'] = ["How can I assist you?"]
    
    if 'requests' not in st.session_state:
        st.session_state['requests'] = []
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=keyy)
    
    if 'buffer_memory' not in st.session_state:
                st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3,return_messages=True)
    
    
    system_msg_template = SystemMessagePromptTemplate.from_template(template="""Answer the question as truthfully as possible using the provided context In Arabic only with now more than 50 words, 
    and if the answer is not contained within the text below, say 'I don't know'""")
    
    
    human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")
    
    prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])
    
    conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)
    
    
    
    
    # container for chat history
    
    response_container = st.container()
    # container for text box
    
    textcontainer = st.container()
    
    
    mytext = audio.audiorec_demo_app()
    
    def change_my_text_back():
        mytext='default'
        
    
    with textcontainer:
        if mytext == 'default':
            query = st.text_input("Question: ", key="input", on_change=change_my_text_back)
        else:
            query = st.text_input("Question: ", key="input", value=mytext, on_change=change_my_text_back)
        if query:
            with st.spinner("typing..."):
                conversation_string = get_conversation_string()
                #st.code(conversation_string)
                refined_query = query_refiner(conversation_string, query)
                #st.subheader("Refined Query:")
                #st.write(refined_query)
                context = find_match(refined_query)
                # print(context)  
                response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query}")
            st.session_state.requests.append(query)
            st.session_state.responses.append(response) 
    with response_container:
        if st.session_state['responses']:
    
            for i in range(len(st.session_state['responses'])):
                message(st.session_state['responses'][i],key=str(i))
                if i < len(st.session_state['requests']):
                    message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')


