import streamlit as st
import requests

# -------------------------------------------------------------------------
# API Configuration
# -------------------------------------------------------------------------
API_BASE_URL = "https://testing.drishtigpt.com/v1/chat-messages"

# IMPORTANT: Make sure your Streamlit secrets have a key named "API_KEY"
#            containing your valid key. e.g.:
#   [secrets]
#   API_KEY="123456XYZ"
API_KEY = st.secrets["API_KEY"]


def send_chat_request(video_id, request_type, query="."):
    """
    Send a chat request to the DrishtiGPT API.
    
    Args:
        video_id (str): The ID of the video (e.g. '7781').
        request_type (str): The type of request (e.g. "summary", "quiz", etc.).
        query (str): The user query or prompt.

    Returns:
        str: The response from the API or an error message.
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "query": query,
        "inputs": {"video_id": video_id, "request_type": request_type},
        "response_mode": "blocking",
        "conversation_id": "",
        "user": "abc-123",  # Replace with a real user/session ID if needed
    }
    response = requests.post(API_BASE_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get("answer", "No response available.")
    else:
        return f"Error: {response.status_code} - {response.json().get('message', response.text)}"


# -------------------------------------------------------------------------
# Streamlit App Layout
# -------------------------------------------------------------------------
st.set_page_config(page_title="DrishtiGPT", layout="wide")

# Sidebar for Video Selection
st.sidebar.title("DrishtiGPT")
video_ids = ["7781", "7782", "7783"]
selected_video_id = st.sidebar.selectbox("Select Video ID", video_ids)

# Main Video Placeholder
st.markdown(f"""
    <div style="display: flex; justify-content: center; align-items: center; 
                height: 300px; background-color: #f0f0f0; border: 1px solid #ccc; 
                margin-bottom: 20px;">
        <p>Video Placeholder - Video ID: {selected_video_id}</p>
    </div>
""", unsafe_allow_html=True)

# Initialize Toggle Menu State
if "menu_visible" not in st.session_state:
    st.session_state.menu_visible = False

def toggle_menu():
    """Toggle the pop-up menu above the + button."""
    st.session_state.menu_visible = not st.session_state.menu_visible

# -------------------------------------------------------------------------
# Custom CSS for Input, Button, and Menu
# -------------------------------------------------------------------------
st.markdown("""
    <style>
    /* 
      The container that holds BOTH the text input and the + button,
      pinned at bottom center of the page.
    */
    .action-container {
        display: flex;
        justify-content: center;
        align-items: center;
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 999;  /* ensure it's on top */
    }

    /* 
      A wrapper for the text input so it can grow (optional).
      This helps keep the input separate from the button container.
    */
    .input-wrapper {
        margin-right: 10px;  /* some spacing to the left of the button */
    }
    .input-wrapper > div > input {
        width: 300px;
        max-width: 300px;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
    }

    /* 
      Container for the + button and the popup menu 
      so we can position the menu absolutely relative to this container.
    */
    .button-container {
        position: relative;
    }

    /* 
      Style the built-in Streamlit button to look like a round + icon.
      We'll place an icon as a background image in the button.
    */
    div[data-testid="stButton"] > button {
        width: 50px;
        height: 50px;
        border-radius: 25px;
        background-color: #007bff !important; /* a nice blue color */
        background-image: url("https://img.icons8.com/ios-glyphs/30/ffffff/plus-math.png");
        background-repeat: no-repeat;
        background-position: center;
        background-size: 20px 20px;
        border: none;
        cursor: pointer;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        color: transparent; /* hide default text (a blank space) */
    }

    /* 
      The pop-up menu, absolutely placed so it appears above the + button.
      bottom: 60px ensures it sits above the 50px button plus some margin.
    */
    .menu {
        position: absolute;
        bottom: 60px;
        left: 50%;
        transform: translateX(-50%);
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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
        font-size: 16px;
    }
    .menu button:hover {
        background-color: #f0f0f0;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# Bottom Input + Toggle (+) Button
# -------------------------------------------------------------------------
st.markdown('<div class="action-container">', unsafe_allow_html=True)

# Text Input to the left
st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
user_query = st.text_input("", placeholder="Type your query...", key="chat_input", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# + Button and (conditionally) the menu
st.markdown('<div class="button-container">', unsafe_allow_html=True)
if st.button(" ", key="toggle_button"):
    toggle_menu()

# If toggled, show the pop-up menu
if st.session_state.menu_visible:
    st.markdown("""
        <div class="menu">
            <button onclick="alert('Summary')">Summary</button>
            <button onclick="alert('Quiz Me')">Quiz Me</button>
            <button onclick="alert('Ask a Question')">Ask a Question</button>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------------------------
# Example Usage: API calls
# -------------------------------------------------------------------------
# If the user typed a query, we can process it.
if user_query:
    # For demonstration, request a "summary" from the API
    response = send_chat_request(selected_video_id, "summary", user_query)
    st.write("**API Response**:", response)
