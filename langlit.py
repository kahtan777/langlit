from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import streamlit as st
from streamlit_chat import message
from utils import *

keyy = st.secrets["openAI_key"]

# Define your video HTML
video_html = """
<style>
.video-container {
    position: fixed; /* Fixed position to keep it in the top left corner */
    top: 0;
    left: 0;
    width: 30%; /* Adjust the width to your desired size */
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
    <source src="https://futurelaby.com/mZaher/80e038fc-7500-41c0-9c7c-595008e2e8bb.mp4">
    Your browser does not support HTML5 video.
</video>
</div>
"""

# Create a container for the entire content and move it to the right
content_container = st.container()

content_container.markdown(
    """
    <style>
    .content-container {
        margin-left: auto;  /* Move the container to the right */
    }
    </style>
    """, unsafe_allow_html=True
)

# Include video and other content in the content_container
content_container.markdown(video_html, unsafe_allow_html=True)

content_container.subheader("Chatbot with Langchain, ChatGPT, Pinecone, and Streamlit")

# Initialize session state variables
if 'responses' not in st.session_state:
    st.session_state['responses'] = ["How can I assist you?"]

if 'requests' not in st.session_state:
    st.session_state['requests'] = []

llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=keyy)

if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

system_msg_template = SystemMessagePromptTemplate.from_template(
    template="""Answer the question as truthfully as possible using the provided context in Arabic only, 
    and if the answer is not contained within the text below, say 'I don't know'"""
)

human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)

# Create a container for chat history
response_container = content_container.container()

# Create a container for the text input
textcontainer = content_container.container()

with textcontainer:
    query = st.text_input("Query: ", key="input")
    if query:
        with st.spinner("typing..."):
            conversation_string = get_conversation_string()
            # st.code(conversation_string)
            refined_query = query_refiner(conversation_string, query)
            st.subheader("Refined Query:")
            st.write(refined_query)
            context = find_match(refined_query)
            response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query}")
        st.session_state.requests.append(query)
        st.session_state.responses.append(response)

with response_container:
    if st.session_state['responses']:
        for i in range(len(st.session_state['responses'])):
            message(st.session_state['responses'][i], key=str(i))
            if i < len(st.session_state['requests']):
                message(st.session_state["requests"][i], is_user=True, key=str(i) + '_user')
