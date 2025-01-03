import streamlit as st
import requests
import json

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


def parse_quiz_data(raw_data):
    """
    Parses raw quiz JSON data, handling errors gracefully.
    """
    try:
        # Handle cases where JSON is improperly formatted
        data = json.loads(f"[{raw_data.replace('}{', '},{')}]")
        return data
    except Exception as e:
        st.error(f"Failed to parse quiz data: {e}")
        return None


def render_quiz(quiz_data):
    """
    Renders the quiz dynamically based on the JSON response.
    """
    if not quiz_data:
        st.error("No valid quiz data available.")
        return

    st.subheader("Quiz Me")
    user_answers = []

    for idx, question in enumerate(quiz_data, start=1):
        st.markdown(f"### {idx}. {question['Question']}")
        options = [
            question["Option 1"],
            question["Option 2"],
            question["Option 3"],
            question["Option 4"],
        ]
        user_answer = st.radio(
            f"Select your answer for Question {idx}:",
            options,
            key=f"q_{idx}",
        )
        user_answers.append({
            "user_answer": user_answer,
            "correct_answer": question["Correct Answer"],
            "explanation": question["Explanation"]
        })

    if st.button("Submit Quiz"):
        st.markdown("### Quiz Results")
        for idx, answer in enumerate(user_answers, start=1):
            if answer["user_answer"] == answer["correct_answer"]:
                st.success(f"✅ Question {idx}: Correct")
            else:
                st.error(f"❌ Question {idx}: Incorrect")
            st.markdown(f"**Your Answer:** {answer['user_answer']}")
            st.markdown(f"**Correct Answer:** {answer['correct_answer']}")
            st.markdown(f"**Explanation:** {answer['explanation']}")


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
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
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

# Summary Button
with col1:
    if st.button("Summary"):
        st.subheader("Video Summary")
        with st.spinner("Fetching summary..."):
            summary_response = send_chat_request(selected_video_id, "Summary")
        if "Error" not in summary_response:
            st.success("Summary fetched successfully!")
            st.components.v1.html(summary_response, height=500, scrolling=True)
        else:
            st.error(summary_response)

# Quiz Me Button
with col2:
    if st.button("Quiz Me"):
        st.subheader("Quiz Me")
        with st.spinner("Fetching quiz..."):
            quiz_response = send_chat_request(selected_video_id, "Quiz Me")
        if "Error" not in quiz_response:
            parsed_data = parse_quiz_data(quiz_response)
            render_quiz(parsed_data)
        else:
            st.error(quiz_response)

# Placeholder for Ask a Question
with col3:
    if st.button("Ask a Doubt"):
        st.subheader("Ask a Doubt")
        st.info("Ask Doubt functionality will be implemented here.")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Developed by DrishtiGPT Team")
