import streamlit as st
import requests

# -------------------------------------------------------------------------
# 1. API Configuration
# -------------------------------------------------------------------------
API_BASE_URL = "https://testing.drishtigpt.com/v1/chat-messages"
API_KEY = st.secrets["API_KEY"]  # Ensure this is set in your Streamlit secrets


def send_chat_request(video_id, request_type, query="."):
    """
    Sends a chat request to the DrishtiGPT API.
    
    Args:
        video_id (str): The ID of the video (e.g., '7781').
        request_type (str): The type of request (e.g., "summary", "quiz", etc.).
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
# 2. Streamlit Layout
# -------------------------------------------------------------------------
st.set_page_config(page_title="DrishtiGPT", layout="wide")

# 2a. Sidebar with Video Selection
st.sidebar.title("DrishtiGPT")
video_ids = ["7781", "7782", "7783"]
selected_video_id = st.sidebar.selectbox("Select Video ID", video_ids)

# 2b. Main Video Placeholder
st.markdown(f"""
    <div style="display: flex; justify-content: center; align-items: center; 
                height: 300px; background-color: #f0f0f0; border: 1px solid #ccc; 
                margin-bottom: 20px;">
        <p>Video Placeholder - Video ID: {selected_video_id}</p>
    </div>
""", unsafe_allow_html=True)

# 2c. Session State for Pop-up Menu
if "menu_visible" not in st.session_state:
    st.session_state.menu_visible = False

def toggle_menu():
    """Toggles the pop-up menu above the + button."""
    st.session_state.menu_visible = not st.session_state.menu_visible

# -------------------------------------------------------------------------
# 3. Custom CSS for Bottom UI (Text Input + Button + Menu)
# -------------------------------------------------------------------------
st.markdown("""
    <style>
    /* 3a. Overall container pinned at bottom center */
    .action-container {
        display: flex;
        justify-content: center;
        align-items: center;
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 999; /* ensure it's above main page content */
    }

    /* 3b. Text Input wrapper */
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

    /* 3c. Button container: relative so we can place the menu absolutely */
    .button-container {
        position: relative;
    }

    /* Remove default Streamlit button container margin/padding if needed */
    div[data-testid="stButton"] {
        margin: 0 !important;
        padding: 0 !important;
    }

    /* 3d. The round + button */
    div[data-testid="stButton"] > button {
        width: 50px;
        height: 50px;
        border-radius: 25px;
        background-color: #007bff !important;
        background-image: url("https://img.icons8.com/ios-glyphs/30/ffffff/plus-math.png");
        background-repeat: no-repeat;
        background-position: center;
        background-size: 20px 20px;
        border: none;
        cursor: pointer;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        color: transparent; /* hide default text */
    }

    /* 3e. The pop-up menu above the button using negative top offset */
    .menu {
        position: absolute;
        left: 50%;
        top: -130px; /* adjust this to move the popup closer/further above the button */
        transform: translateX(-50%);
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
        padding: 10px;
        z-index: 9999999; /* ensure it's on top */
        pointer-events: auto; /* ensure clickable in some Streamlit setups */
        min-width: 120px; /* ensure enough width for menu options */
    }

    /* 3f. Styling the buttons inside the pop-up menu */
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
# 4. Bottom-Center UI: Text Input + +Button + Popup
# -------------------------------------------------------------------------
st.markdown('<div class="action-container">', unsafe_allow_html=True)

# 4a. Text Input
st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
user_query = st.text_input(
    "",
    placeholder="Type your query...",
    key="chat_input",
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# 4b. The + button & pop-up menu
st.markdown('<div class="button-container">', unsafe_allow_html=True)

if st.button(" ", key="toggle_menu_btn"):
    toggle_menu()

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

# -------------------------------------------------------------------------
# 5. Example: Using the user query to call the API
# -------------------------------------------------------------------------
if user_query:
    # For demonstration, let's request a "summary" from the API
    response = send_chat_request(selected_video_id, "summary", user_query)
    st.write("**API Response**:", response)
