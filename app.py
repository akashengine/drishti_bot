import streamlit as st
import requests

# -------------------------------------------------------------------------
# API Configuration
# -------------------------------------------------------------------------
API_BASE_URL = "https://testing.drishtigpt.com/v1/chat-messages"
# Make sure your Streamlit secrets has a key named "API_KEY" with your valid API key.
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

# Session state for pop-up menu
if "menu_visible" not in st.session_state:
    st.session_state.menu_visible = False

def toggle_menu():
    """Toggle the pop-up menu above the + button."""
    st.session_state.menu_visible = not st.session_state.menu_visible

# -------------------------------------------------------------------------
# Custom CSS
# -------------------------------------------------------------------------
st.markdown("""
    <style>
    /* 
      action-container: pinned at bottom center
      holds the text input + button container
    */
    .action-container {
        display: flex;
        justify-content: center;
        align-items: center;
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 999; /* Keep on top of page content */
    }

    /* input-wrapper: just wraps the text input field */
    .input-wrapper {
        margin-right: 10px;
    }
    .input-wrapper > div > input {
        width: 300px;
        max-width: 300px;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
    }

    /* 
      button-container: relative positioning so we can absolutely
      position the menu. 
    */
    .button-container {
        position: relative;
    }

    /* Remove default Streamlit button margin/padding if needed */
    div[data-testid="stButton"] {
        margin: 0 !important;
        padding: 0 !important;
    }

    /*
      The round + button:
      We style Streamlit's built-in button to appear as a circle
      with a plus icon in the middle.
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
        color: transparent; /* hides the default text (which is just a space) */
    }

    /*
      The pop-up menu. Instead of positioning from the bottom,
      we'll place it above the button by using top + negative offset.
      We'll nudge it just enough to appear directly above the circle.

      top: auto;
      bottom: auto; (not used)

      We set "top: -120px" or so from the top of the .button-container.
      Adjust the number to get the exact vertical spacing you prefer.
    */
    .menu {
        position: absolute;
        left: 50%;
        top: -130px; /* adjust to position exactly above the button */
        transform: translateX(-50%);
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
        padding: 10px;
        z-index: 1000;
        min-width: 120px; /* ensure some width for the menu */
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
# Layout at the bottom center
# -------------------------------------------------------------------------
st.markdown('<div class="action-container">', unsafe_allow_html=True)

# The text input field
st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
user_query = st.text_input(
    "",
    placeholder="Type your query...",
    key="chat_input",
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# The + button and pop-up container
st.markdown('<div class="button-container">', unsafe_allow_html=True)

if st.button(" ", key="toggle_menu_btn"):
    toggle_menu()

# The pop-up menu, if visible
if st.session_state.menu_visible:
    st.markdown("""
        <div class="menu">
            <button onclick="alert('Summary')">Summary</button>
            <button onclick="alert('Quiz Me')">Quiz Me</button>
            <button onclick="alert('Ask a Question')">Ask a Question</button>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close .button-container
st.markdown('</div>', unsafe_allow_html=True)  # close .action-container
