import streamlit as st
import requests
import time

st.set_page_config(page_title="AI Food Agent", page_icon="🍔", layout="centered")

st.title("🤖 Agentic Food Ordering System")
st.markdown("**Multi-Agent AI** powered by CrewAI + Gemini")

# Custom CSS for better look
st.markdown("""
<style>
    .stChatMessage {border-radius: 15px;}
    .user-message {background-color: #2E8B57; color: white;}
</style>
""", unsafe_allow_html=True)

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Namaste! 👋 Aaj kya order karna chahte ho? (Butter chicken, biryani, etc.)"}
    ]


# Chat History Display
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# User Input
if prompt := st.chat_input("Apna order yahan type karo..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    
    # Show typing indicator
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")


        try:
            response = requests.post(
                "http://127.0.0.1:8000/api/order",
                json={"message": prompt},
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                result = data.get("data", {}).get("result", "Sorry, kuch samajh nahi aaya.")
                message_placeholder.markdown(result)
                st.session_state.messages.append({"role": "assistant", "content": result})
            else:
                message_placeholder.error("Server error! FastAPI running hai kya?")
            
        
        except requests.exceptions.ConnectionError:
            message_placeholder.error("❌ FastAPI server connect nahi ho raha. `uvicorn app.main:app --reload` chal raha hai?")
        except Exception as e:
            message_placeholder.error(f"Error: {e}")


# Sidebar
with st.sidebar:
    st.header("Controls")
    if st.button("Clear Chat History"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Chat cleared! Aaj kya order karna hai bhai? 🍛"}
        ]
        st.rerun()
    
    st.info("**Tips:**\n- Butter chicken with 2 naan\n- Paneer butter masala\n- Yes / Haan / Confirm bol ke order place kar sakte ho")

st.caption("Built with CrewAI + Gemini + FastAPI + Streamlit")