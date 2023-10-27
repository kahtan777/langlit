import streamlit as st
from streamlit_chat import message
from utils import *

# Add this CSS code to your Streamlit app
st.markdown("""
<style>
    .textcontainer {
        float: right;
        width: 50%;
    }

    .response-container {
        float: right;
        width: 50%;
    }
</style>
""", unsafe_allow_html=True)

st.subheader("Chatbot with Langchain, ChatGPT, Pinecone, and Streamlit")

if 'responses' not in st.session_state:
    st.session_state['responses'] = ["How can I assist you?"]

if 'requests' not in st.session_state:
    st.session_state['requests'] = []

keyy = st.secrets["openAI_key"]

llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=keyy)

if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

system_msg_template = SystemMessagePromptTemplate.from_template("""Answer the question as truthfully as possible using the provided context in Arabic only, 
and if the answer is not contained within the text below, say 'I don't know'"")

human_msg_template = HumanMessagePromptTemplate.from_template("{input}")

prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)

# container for chat history
st.markdown('<div class="textcontainer">', unsafe_allow_html=True)
query = st.text_input("Query: ", key="input")
if query:
    with st.spinner("typing..."):
        conversation_string = get_conversation_string()
        refined_query = query_refiner(conversation_string, query)
        st.subheader("Refined Query:")
        st.write(refined_query)
        context = find_match(refined_query)
        response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query}")
    st.session_state.requests.append(query)
    st.session_state.responses.append(response)
st.markdown('</div>', unsafe_allow_html=True)

# container for chat history
st.markdown('<div class="response-container">', unsafe_allow_html=True)
if st.session_state['responses']:
    for i in range(len(st.session_state['responses'])):
        message(st.session_state['responses'][i], key=str(i))
        if i < len(st.session_state['requests']):
            message(st.session_state["requests"][i], is_user=True, key=str(i) + '_user')
st.markdown('</div>', unsafe_allow_html=True)
