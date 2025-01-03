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

# CSS for Styling
st.markdown("""
    <style>
    .main-container {
        max-width: 800px;
        margin: auto;
    }
    .video-placeholder {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 300px;
        background-color: #f0f0f0;
        border: 1px solid #ccc;
        margin-bottom: 20px;
    }
    .action-container {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        align-items: center;
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
        color: white;
        font-size: 24px;
        font-weight: bold;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
    }
    .menu {
        position: fixed;
        bottom: 90px;
        left: 50%;
        transform: translateX(-50%);
        background-color: white;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
        padding: 10px;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .menu button {
        border: none;
        background: none;
        padding: 10px;
        text-align: left;
        cursor: pointer;
        font-size: 16px;
    }
    .menu button:hover {
        background-color: #f0f0f0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("DrishtiGPT")
video_ids = ["7781", "7782", "7783"]  # Dummy Video IDs
selected_video_id = st.sidebar.selectbox("Select Video ID", video_ids)

# Main Content
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown(f"""
    <div class="video-placeholder">
        <p>Video Placeholder - Video ID: {selected_video_id}</p>
    </div>
""", unsafe_allow_html=True)

# Initialize Menu State
if "menu_visible" not in st.session_state:
    st.session_state.menu_visible = False

# Toggle Menu Visibility
def toggle_menu():
    st.session_state.menu_visible = not st.session_state.menu_visible

# Input and Toggle Button
st.markdown('<div class="action-container">', unsafe_allow_html=True)

# Chat Input
user_query = st.text_input("", placeholder="Type your query...", key="chat_input", label_visibility="collapsed", help="Ask your question here!")

# Action Button
if st.button("+", key="toggle_button"):
    toggle_menu()

st.markdown('</div>', unsafe_allow_html=True)

# Pop-Up Menu
if st.session_state.menu_visible:
    st.markdown('<div class="menu">', unsafe_allow_html=True)
    if st.button("Summary"):
        with st.spinner("Fetching summary..."):
            summary_response = send_chat_request(selected_video_id, "Summary")
        if "Error" not in summary_response:
            st.success("Summary fetched successfully!")
            st.components.v1.html(summary_response, height=500, scrolling=True)
        else:
            st.error(summary_response)
    if st.button("Quiz Me"):
        with st.spinner("Fetching quiz..."):
            quiz_response = send_chat_request(selected_video_id, "Quiz")
        if "Error" not in quiz_response:
            st.success("Quiz fetched successfully!")
            st.markdown(quiz_response, unsafe_allow_html=True)
        else:
            st.error(quiz_response)
    if st.button("Ask a Question"):
        st.info("Ask a Question functionality coming soon.")
    st.markdown('</div>', unsafe_allow_html=True)
