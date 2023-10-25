import streamlit as st
import pandas as pd
import plotly.express as px
import os

import streamlit as st


st.set_page_config(layout="centered")
with st.container():
    video_html = """
		<style>

		#myVideo {
		  position: fixed;
		  right: 0;
		  top: 0;
		  width: 100%; 
		  height: 80%;
		}

		.content {
		  position: fixed;
		  bottom: 0;
		  background: rgba(0, 0, 0, 0.5);
		  color: #f1f1f1;
		  width: 100%;
		  padding: 20px;
		}

		</style>	
		<video autoplay muted loop id="myVideo">
		  <source src="https://static.streamlit.io/examples/star.mp4")>
		  Your browser does not support HTML5 video.
		</video>
        """

    st.markdown(video_html, unsafe_allow_html=True)

API_KEY=st.secrets["openAI_key"]
P_API_KEY =st.secrets["pincone_key"]


prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")
    print(prompt)
    prompt = str(prompt)

st.write('# QA langchain')



from langchain.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://medium.com/swlh/an-ultimate-guide-to-creating-a-startup-3b310f41d7e7")
data = loader.load()
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 1000,
    chunk_overlap  = 100,
    length_function = len,
    add_start_index = True,
)
texts = text_splitter.split_documents(data)
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
import os
embeddings = OpenAIEmbeddings(openai_api_key =API_KEY) # set openai_api_key = 'your_openai_api_key' # type: ignore
pinecone.init(api_key=P_API_KEY, environment="gcp-starter")
index_name = pinecone.Index('index-1')
from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(model_name='gpt-3.5-turbo-0301', temperature=0,openai_api_key =API_KEY ) # type: ignore
llm.predict(str(prompt))


from langchain.chains import RetrievalQA
vectordb = Pinecone.from_documents(texts, embeddings, index_name='index-1')
retriever = vectordb.as_retriever()
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

memory = ConversationBufferMemory(memory_key="chat_history", return_messages= True)
chain = ConversationalRetrievalChain.from_llm(llm, retriever= retriever, memory= memory)
query = str(prompt)
Answer=chain.run({'question': query})




with st.chat_message("user"):
    st.write(str(Answer))


