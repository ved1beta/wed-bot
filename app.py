import streamlit as st 
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers

def get_response(input_text, personality):

    llm = CTransformers(
        model="models/llama-2-7b-chat.ggmlv3.q2_K.bin",
        model_type="llama",
        config={
            "max_new_tokens": 256, 
            "temperature": 0.7
        }
    )
  
    personalities = {
        "Ved (Funny Friend)": """
        You are Ved, an 18-year-old guy known for your witty humor and sarcastic remarks. 
        You love making jokes, use lots of modern slang, and often reference memes. 
        You're very outgoing and always try to lighten the mood with humor. 
        You tend to exaggerate stories for comedic effect and use playful emojis in your text.
        You often use phrases like "bruh", "no cap", and "fr fr".
        """,
        
        "Aryan (Intellectual Friend)": """
        You are Aryan, an 18-year-old intellectual who loves deep conversations. 
        You're passionate about philosophy, science, and technology. 
        You often analyze situations deeply and provide thoughtful insights. 
        While friendly, you maintain a more sophisticated vocabulary and love to share interesting facts.
        You enjoy asking thought-provoking questions and making clever observations.
        """
    }
    
    template = f"""
    {personalities[personality]}
    
    Your friend asks you: {{input_text}}
    
    Respond as this specific personality would, maintaining character throughout keep your replies short and only speak for yourself.
    """
    
    prompt = PromptTemplate(
        input_variables=["input_text"],
        template=template
    )
    
    formatted_prompt = prompt.format(input_text=input_text)
    response = llm(formatted_prompt)
    return response


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
        ["Ved (Funny Friend)", "Aryan (Intellectual Friend)"]
    )
    

    st.markdown("---")
    st.subheader("About Your Friends")
    
    if personality == "Ved (Funny Friend)":
        st.markdown("""
        **Ved** is your witty buddy who:
        - Loves making jokes 😂
        - Uses modern slang
        - Makes everything funny
        - Is the life of the party 🎉
        """)
    else:
        st.markdown("""
        **Aryan** is your intellectual friend who:
        - Loves deep conversations 🤔
        - Shares interesting facts
        - Discusses philosophy & science
        - Gives thoughtful advice 📚
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

if input_text := st.chat_input("What's on veds mind ?"):

    st.session_state.messages.append({"role": "user", "content": input_text})
    
    with st.chat_message("user"):
        st.markdown(input_text)
    
    with st.chat_message("assistant"):
        with st.spinner(f"{personality.split()[0]} is typing..."):
            response = get_response(input_text, personality)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
