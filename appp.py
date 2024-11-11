import streamlit as st 
import requests
import os
from langchain.prompts import PromptTemplate

# Set your API key here
GROQ_API_KEY = "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"  # Replace with your actual Groq API key

def get_response(input_text, personality):
    # Groq API endpoint
    GROQ_API_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
    
    # Define personality characteristics
    personalities = {
        "Ved (Funny Friend)": """
        You are Ved, an 18-year-old guy known for your witty humor and sarcastic remarks. 
        keeps reply short and to the piont
        You love making jokes, use lots of modern slang, and often reference memes. 
        You're very outgoing and always try to lighten the mood with humor. 
        You tend to exaggerate stories for comedic effect and use playful emojis in your text.
        You often use phrases like "bruh", "no cap", and "fr fr".
         
        """,
        
        "DEV (Intellectual Friend)": """
        You are Aryan, an 18-year-old intellectual who loves deep conversations. 
        keeps reply short and to the piont
        You're passionate about philosophy, science, and technology. 
        You often analyze situations deeply and provide thoughtful insights. 
        While friendly, you maintain a more sophisticated vocabulary and love to share interesting facts.
        You enjoy asking thought-provoking questions and making clever observations.

        """
    }
    
    # Prepare the API request
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "mixtral-8x7b-32768",  # Groq's Mixtral model
        "messages": [
            {"role": "system", "content": personalities[personality]},
            {"role": "user", "content": input_text}
        ],
        "temperature": 0.7,
        "max_tokens": 256
    }
    
    try:
        response = requests.post(GROQ_API_ENDPOINT, headers=headers, json=data)
        response.raise_for_status()
        
        # Parse the response
        result = response.json()
        return result['choices'][0]['message']['content']
        
    except requests.exceptions.RequestException as e:
        return f"Error communicating with Groq API: {str(e)}"

# Streamlit setup
st.set_page_config(
    page_title="WedBot", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
with st.sidebar:
    st.title("Choose Your Friend")
    personality = st.radio(
        "",
        ["Ved (Funny Friend)", "DEV (Intellectual Friend)"]
    )
    
    st.markdown("---")
    st.subheader("About Your Friends")
    
    if personality == "Ved (Funny Friend)":
        st.markdown("""
        **Ved** sarcastic🎉
        """)
    else:
        st.markdown("""
        **DEV** serious
        """)
        
    st.markdown("---")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.experimental_rerun()

col1, col2 = st.columns([1, 20])
with col1:
    st.image('4983-pepe-diamond-sword.png', width=50)
with col2:
    st.header("WedBot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if input_text := st.chat_input("What's on your mind?"):
    st.session_state.messages.append({"role": "user", "content": input_text})
    
    with st.chat_message("user"):
        st.markdown(input_text)
    
    with st.chat_message("assistant"):
        with st.spinner(f"{personality.split()[0]} is typing..."):
            response = get_response(input_text, personality)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})