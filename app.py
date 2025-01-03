import streamlit as st
import requests

# API Configuration
API_BASE_URL = "https://testing.drishtigpt.com/v1/chat-messages"
API_KEY = st.secrets["API_KEY"]  # Securely retrieve API Key

def send_chat_request(video_id, request_type, query="."):
    """
    Sends a request to the chat API with the given parameters.
    """
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "query": query,
            "inputs": {
                "video_id": video_id,
                "request_type": request_type
            },
            "response_mode": "blocking",
            "conversation_id": "",
            "user": "abc-123",
        }
        response = requests.post(API_BASE_URL, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json().get("answer", "No response available.")
        else:
            return f"Error: {response.status_code} - {response.json().get('message', response.text)}"
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit App Layout
st.set_page_config(page_title="DrishtiGPT", layout="wide")

# Sidebar for Video Selection
st.sidebar.title("DrishtiGPT")
video_ids = ["7781", "7782", "7783"]  # Dummy Video IDs
selected_video_id = st.sidebar.selectbox("Select Video ID", video_ids)

# Main Content: Video Placeholder
st.markdown(f"""
    <div style="display: flex; justify-content: center; align-items: center; height: 300px; background-color: #f0f0f0; border: 1px solid #ccc; margin-bottom: 20px;">
        <p>Video Placeholder - Video ID: {selected_video_id}</p>
    </div>
""", unsafe_allow_html=True)

# Initialize Menu State
if "menu_visible" not in st.session_state:
    st.session_state.menu_visible = False

# Toggle Function
def toggle_menu():
    st.session_state.menu_visible = not st.session_state.menu_visible

# CSS Styling for Alignment and Button
st.markdown("""
    <style>
    .action-container {
        display: flex;
        align-items: center;
        justify-content: center;
        position: fixed;
        bottom: 20px;
        width: 100%;
    }
    .chat-input {
        width: 300px;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        margin-right: 10px;
    }
    .action-button {
        width: 60px;
        height: 60px;
        border-radius: 30px;
        background-color: #007bff;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .action-button img {
        width: 30px;
        height: 30px;
    }
    .menu {
        position: fixed;
        bottom: 90px;
        right: 20px;
        background-color: white;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
        padding: 10px;
        z-index: 1000;
    }
    .menu button {
        display: block;
        width: 100%;
        margin-bottom: 10px;
        background: none;
        border: none;
        text-align: left;
        cursor: pointer;
    }
    .menu button:hover {
        background-color: #f0f0f0;
    }
    </style>
""", unsafe_allow_html=True)

# Input and Action Button Layout
st.markdown('<div class="action-container">', unsafe_allow_html=True)

# Chat Input
user_query = st.text_input("", placeholder="Type your query...", key="chat_input", label_visibility="collapsed")

# Action Button with Icon
if st.button("+", key="toggle_button"):
    toggle_menu()
st.markdown("""
    <div class="action-button" onclick="toggleMenu()">
        <img src="https://img.icons8.com/ios-glyphs/30/e74c3c/plus-math.png" alt="Add">
    </div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Pop-Up Menu
if st.session_state.menu_visible:
    st.markdown("""
        <div class="menu">
            <button onclick="alert('Summary')">Summary</button>
            <button onclick="alert('Quiz Me')">Quiz Me</button>
            <button onclick="alert('Ask a Question')">Ask a Question</button>
        </div>
    """, unsafe_allow_html=True)
