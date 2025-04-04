import requests
import streamlit as st
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from template import css, bot_template, user_template
import os
from datetime import datetime
import dateparser
import re

load_dotenv()
openai_api_key= os.getenv("OPENAI_API_KEY")

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(separator="\n",chunk_size = 1000, chunk_overlap = 200,length_function = len)
    chunks = text_splitter.split_text(text)
    return chunks


def get_conversation_chain(vector_store):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm ,
        memory = memory,
        retriever = vector_store.as_retriever(),

    )
    return conversation_chain


def get_pdf_text(uploaded_files):
    text = ""
    for pdf in uploaded_files:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    
    return text

def get_vector_store(text_chunks):
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vector_store

def validate_phone(phone):
    pattern = r'^\+?\d{10,15}$'
    return re.match(pattern, phone) is not None

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def parsed_date(date_str):
    parsed = dateparser.parse(date_str)
    if parsed and parsed.date() >= datetime.today().date():
        return parsed.strftime("%Y-%m-%d")
    return None

def collect_user_info():
        
        st.subheader("Book an Appointment with us")

        name = st.text_input("Your Name")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email Address")
        date = st.text_input("Preferred Date(eg: next monday , tomorrow, 20 July)")

        submit = st.button("Submit Appointment")

        if submit:
            if not name or not validate_phone(phone) or not validate_email(email):
                st.error("Please enter valid name , email, and number")
                return None
            
            appointment_date = parsed_date(date)


            if not appointment_date:
                st.error("Please enter a valid future date")
                return None
            return f"Appointment Booked!!! \n\n Name:{name} \n\n Phone:{phone} \n\n Email:{email} \n\n Date:{appointment_date}"
        return None



def handle_input_text(input_text):

    if "appointment_message" not in st.session_state:
        st.session_state.appointment_message = None

    if "call" in input_text.lower() or "book" in input_text.lower():
        st.write(user_template.replace("{{MSG}}", input_text), unsafe_allow_html=True)
        st.write(bot_template.replace("{{MSG}}", "Let's book an appointment! Please fill out the form below:"), unsafe_allow_html=True)
        response = collect_user_info()

        if response:
            st.session_state.appointment_message = response
        
        if st.session_state.appointment_message:
            st.write(bot_template.replace("{{MSG}}", st.session_state.appointment_message), unsafe_allow_html=True)
        return
                
    if st.session_state.conversation is None:
        st.warning("Please upload and process PDF documents first to enable the chatbot.")
        return

    response = st.session_state.conversation({'question':input_text})
    st.session_state.chat_history = response["chat_history"]

    for i, message in enumerate(st.session_state.chat_history):
        if i  % 2 ==0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)



def get_openai_response(input_text):
    response = requests.post("http://localhost:8000/generate",
    json={'prompt':input_text,'max_tokens':100})

    return response.json()['response']


with st.sidebar:
    st.markdown("📌 Try saying: *Call* or *Book* to schedule an appointment")

    st.write(css, unsafe_allow_html=True)
  
    st.sidebar.title("Your documents")
    uploaded_files = st.sidebar.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if st.sidebar.button("Process") and uploaded_files:
        raw_text = get_pdf_text(uploaded_files)
        text_chunks = get_text_chunks(raw_text)
        vector_store = get_vector_store(text_chunks)

        st.session_state.conversation = get_conversation_chain(vector_store)

        st.sidebar.success("Files uploaded!")
    

if "conversation" not in st.session_state:
    st.session_state.conversation = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = None

if "appointment_message" not in st.session_state:
    st.session_state.appointment_message = None

st.title("DemoGpt")
input_text = st.text_input("What can I help you with?")

if input_text:
    handle_input_text(input_text)
    


