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

API_KEY = st.secrets["openAI_key"]
P_API_KEY = st.secrets["pincone_key"]

loader = WebBaseLoader("https://medium.com/swlh/an-ultimate-guide-to-creating-a-startup-3b310f41d7e7")
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=1000,
    chunk_overlap=100,
    length_function=len,
    add_start_index=True,
)
texts = text_splitter.split_documents(data)

embeddings = OpenAIEmbeddings(openai_api_key=API_KEY)
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

conversation_history = []  # Initialize conversation history list

prompt = st.chat_input("Say something")
if prompt:
    with st.chat_message("user"):
        st.write(str(prompt))

llm = ChatOpenAI(model_name='gpt-3.5-turbo-0301', temperature=0, openai_api_key=API_KEY)
llm.predict(str(prompt))

vectordb = Pinecone.from_documents(texts, embeddings, index_name='index-1')
retriever = vectordb.as_retriever()

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
chain = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)
query = str(prompt)
Answer = chain.run({'question': query})

if prompt:
    conversation_history.append(("user", str(prompt)))

if Answer:
    conversation_history.append(("assistant", str(Answer)))

# Display the full chat history

container = st.container()
container.write("This is inside the container")


container.subheader("Chat History")
for role, message in conversation_history:
    if role == "user":
        container.write("User: ", message)
    elif role == "assistant":
        container.write("Assistant: ", message)

st.button("Voice input")
