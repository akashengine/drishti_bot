import streamlit as st
import requests

# API Configuration
API_BASE_URL = "http://testing.drishtigpt.com/v1/chat-messages"
API_KEY = "app-RCjaiFBd7PURraoAZGHmlLC5"

# Fetch Summary from API
def fetch_summary(video_id, user_id="unique-user-id"):
    query = f"Please summarize video ID {video_id}."
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "query": query,
        "inputs": {},
        "response_mode": "blocking",
        "conversation_id": "",
        "user": user_id,
    }
    response = requests.post(API_BASE_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get("answer", "No summary available.")
    else:
        return f"Error: {response.status_code} - {response.text}"

# Streamlit App Layout
st.set_page_config(page_title="DrishtiGPT", layout="wide")

# Sidebar: Video ID Selection
st.sidebar.title("DrishtiGPT")
video_ids = ["7781", "7782", "7783"]  # Dummy Video IDs
selected_video_id = st.sidebar.selectbox("Select Video ID", video_ids)

# Main Section
st.title("DrishtiGPT Video Assistant")
st.subheader(f"Selected Video ID: {selected_video_id}")

# Tab Navigation
tab_options = ["Summary", "Quiz Me", "Ask a Question"]
selected_tab = st.selectbox("Choose an Option", tab_options)

# Summary Tab
if selected_tab == "Summary":
    st.header("Video Summary")
    if st.button("Generate Summary"):
        with st.spinner("Fetching summary..."):
            summary_response = fetch_summary(selected_video_id)
        if "Error" not in summary_response:
            st.success("Summary fetched successfully!")
            st.markdown(summary_response)
        else:
            st.error(summary_response)

# Placeholder for Quiz Me
elif selected_tab == "Quiz Me":
    st.header("Quiz Me")
    st.info("Quiz functionality will be implemented here.")

# Placeholder for Ask a Question
elif selected_tab == "Ask a Question":
    st.header("Ask a Question")
    st.info("Question functionality will be implemented here.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Developed by DrishtiGPT Team")
