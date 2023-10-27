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
keyy=st.secrets["openAI_key"]



video_html = """
<style>
.video-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 70%; /* Make the video 70% of the screen width */
    height: 100%; /* Set the height to 100% to cover the entire height */
}

video {
    width: 100%;
    height: 100%; /* Set the video to cover the entire height of the container */
}

.content {
    background: rgba(0, 0, 0, 0.5);
    color: #f1f1f1;
    width: 30%; /* Allocate 30% of the screen width for content */
    height: 100%; /* Set the height to 100% to cover the entire height */
    position: fixed; /* Keep content fixed to the right */
    top: 0;
    right: 0;
    overflow: auto; /* Add scrolling for content if needed */
}

</style>    
<div class="video-container">
<video autoplay muted loop id="myVideo">
    <source src="https://static.streamlit.io/examples/star.mp4">
    Your browser does not support HTML5 video.
</video>
</div>
<div class="content">
    <!-- Your content here -->
    <h1>Your Content</h1>
    <p>This is your content placed to the right of the video.</p>
</div>
"""

st.markdown(video_html, unsafe_allow_html=True)





st.subheader("Chatbot with Langchain, ChatGPT, Pinecone, and Streamlit")

if 'responses' not in st.session_state:
    st.session_state['responses'] = ["How can I assist you?"]

if 'requests' not in st.session_state:
    st.session_state['requests'] = []

llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=keyy)

if 'buffer_memory' not in st.session_state:
            st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3,return_messages=True)


system_msg_template = SystemMessagePromptTemplate.from_template(template="""Answer the question as truthfully as possible using the provided context in Arabic only, 
and if the answer is not contained within the text below, say 'I don't know'""")


human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)




# container for chat history
response_container = st.container()
# container for text box
textcontainer = st.container()


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
