import streamlit as st
import pandas as pd
import plotly.express as px
import os
import pinecone
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chains import RetrievalQA
from vector_db import Pinecone
from conversation_memory import ConversationBufferMemory
from conversational_retrieval import ConversationalRetrievalChain


API_KEY=st.secrets["openAI_key"]
P_API_KEY =st.secrets["pincone_key"]


loader = WebBaseLoader("https://medium.com/swlh/an-ultimate-guide-to-creating-a-startup-3b310f41d7e7")
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 1000,
    chunk_overlap  = 100,
    length_function = len,
    add_start_index = True,
)
texts = text_splitter.split_documents(data)

embeddings = OpenAIEmbeddings(openai_api_key =API_KEY) # set openai_api_key = 'your_openai_api_key' # type: ignore
pinecone.init(api_key=P_API_KEY, environment="gcp-starter")
index_name = pinecone.Index('index-1')


st.set_page_config(layout="centered")

with st.container():
    video_html = """
    <style>
    .video-container {
    width: 100%; 
    height: auto;
    }

    video {
    width: 100%; 
    height: auto;
    }

    .content {
    background: rgba(0, 0, 0, 0.5);
    color: #f1f1f1;
    width: 100%;
    padding: 20px;
    }
    </style>	
    <div class="video-container">
    <video autoplay muted loop id="myVideo">
        <source src="https://static.streamlit.io/examples/star.mp4">
        Your browser does not support HTML5 video.
    </video>
    </div>
    """  
    st.markdown(video_html, unsafe_allow_html=True) 
    

# Create a function to add messages to the chat history
def add_message(author, text):
    st.session_state.chat_history.append({'author': author, 'text': text})

# Create a function to display the chat history
def display_chat_history():
    with st.container():
        for message in st.session_state.chat_history:
            with st.chat_message(message['author']):
                st.write(message['text'])

# User input
prompt = st.text_input("Say something:", key="user_input")

        
llm = ChatOpenAI(model_name='gpt-3.5-turbo-0301', temperature=0,openai_api_key =API_KEY ) # type: ignore
llm.predict(str(prompt))
vectordb = Pinecone.from_documents(texts, embeddings, index_name='index-1')
retriever = vectordb.as_retriever()
memory = ConversationBufferMemory(memory_key="chat_history", return_messages= True)
chain = ConversationalRetrievalChain.from_llm(llm, retriever= retriever, memory= memory)


if prompt:
    add_message('user', prompt)
    # Get the response from your model
    query = str(prompt)
    Answer = chain.run({'question': query})
    add_message('assistant', Answer)
    # Clear the input field
    st.session_state.user_input = ""


display_chat_history()






