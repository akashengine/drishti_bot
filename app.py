import streamlit as st
import requests

# API Configuration
API_BASE_URL = "http://testing.drishtigpt.com/v1/chat-messages"
API_KEY = st.secrets["API_KEY"]  # Securely retrieve API Key

# Fetch Summary from API
def fetch_summary(video_id, user_id="unique-user-id"):
    """
    Fetches the summary of the selected video from the API.
    """
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "query": f"Please summarize video ID {video_id}.",
            "inputs": {},
            "response_mode": "blocking",
            "conversation_id": "",
            "user": user_id,
        }
        response = requests.post(API_BASE_URL, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json().get("answer", "No summary available.")
        else:
            return f"Error: {response.status_code} - {response.json().get('message', response.text)}"
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit App Layout
st.set_page_config(page_title="DrishtiGPT", layout="wide")

# CSS for Custom Styling
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
    .tabs-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
    }
    .tabs-container button {
        padding: 10px 20px;
        font-size: 14px;
        border: none;
        cursor: pointer;
        border-radius: 5px;
        background-color: #007bff;
        color: white;
    }
    .tabs-container button:hover {
        background-color: #0056b3;
    }
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    .custom-header {
        text-align: center;
        margin-top: 20px;
        font-size: 24px;
        font-weight: bold;
    }
    .sidebar {
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Logo
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
st.image("https://drishtigpt.com/upload/images/logo/ZqUG-dashboard-2x-drishtigpt-logo.svg", width=200)
st.markdown('</div>', unsafe_allow_html=True)

# Sidebar for Video Selection
st.sidebar.title("DrishtiGPT")
st.sidebar.markdown('<div class="sidebar">', unsafe_allow_html=True)
video_ids = ["7781", "7782", "7783"]  # Dummy Video IDs
selected_video_id = st.sidebar.selectbox("Select Video ID", video_ids)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Main Content
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown(f"""
    <div class="video-placeholder">
        <p>Video Placeholder - Video ID: {selected_video_id}</p>
    </div>
""", unsafe_allow_html=True)

# Buttons for Actions
st.markdown('<div class="tabs-container">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Summary"):
        st.subheader("Video Summary")
        with st.spinner("Fetching summary..."):
            summary_response = fetch_summary(selected_video_id)
        if "Error" not in summary_response:
            st.success("Summary fetched successfully!")
            st.markdown(summary_response)
        else:
            st.error(summary_response)

with col2:
    if st.button("Quiz Me"):
        st.subheader("Quiz Me")
        st.info("Quiz functionality will be implemented here.")

with col3:
    if st.button("Ask a Doubt"):
        st.subheader("Ask a Doubt")
        st.info("Ask Doubt functionality will be implemented here.")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Developed by DrishtiGPT Team")
