import streamlit as st
import requests
import json

# API Configuration
API_BASE_URL = "https://testing.drishtigpt.com/v1/chat-messages"
API_KEY = st.secrets["API_KEY"]


def send_chat_request(video_id, request_type, query="."):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "query": query,
        "inputs": {"video_id": video_id, "request_type": request_type},
        "response_mode": "blocking",
        "conversation_id": "",
        "user": "abc-123",
    }
    response = requests.post(API_BASE_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json().get("answer", "No response available.")
    else:
        return f"Error: {response.status_code} - {response.json().get('message', response.text)}"


def parse_quiz_data(raw_data):
    quizzes = []
    try:
        for quiz in raw_data.strip().split("\n\n"):
            quizzes.append(json.loads(quiz))
    except Exception as e:
        st.error(f"Failed to parse quiz data: {e}")
    return quizzes


# App Layout
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
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    .quiz-container {
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
video_ids = ["7781", "7782", "7783"]  # Dummy Video IDs
selected_video_id = st.sidebar.selectbox("Select Video ID", video_ids)

# Main Content
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown(f"""
    <div class="video-placeholder">
        <p>Video Placeholder - Video ID: {selected_video_id}</p>
    </div>
""", unsafe_allow_html=True)

# Manage State for All Functionalities
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = []
if "selected_answers" not in st.session_state:
    st.session_state.selected_answers = {}
if "show_results" not in st.session_state:
    st.session_state.show_results = False
if "summary_data" not in st.session_state:
    st.session_state.summary_data = None
if "doubt_response" not in st.session_state:
    st.session_state.doubt_response = None

# Buttons for Summary, Quiz Me, and Ask a Doubt
col1, col2, col3 = st.columns(3)

# Summary Button
with col1:
    if st.button("Summary"):
        with st.spinner("Fetching summary..."):
            summary_data = send_chat_request(selected_video_id, "Summary")
            st.session_state.summary_data = summary_data

# Display Summary
if st.session_state.summary_data:
    st.subheader("Video Summary")
    st.write(st.session_state.summary_data)

# Quiz Me Button
with col2:
    if st.button("Quiz Me"):
        with st.spinner("Fetching quiz..."):
            raw_quiz_data = send_chat_request(selected_video_id, "Quiz Me")
            st.session_state.quiz_data = parse_quiz_data(raw_quiz_data)
            st.session_state.selected_answers = {}
            st.session_state.show_results = False

# Display Quiz
if st.session_state.quiz_data:
    st.subheader("Take the Quiz")
    for idx, quiz in enumerate(st.session_state.quiz_data):
        question = quiz.get("Question", "No question available.")
        options = [quiz.get(f"Option {i}", "") for i in range(1, 5)]

        # Maintain selected answer state
        if idx not in st.session_state.selected_answers:
            st.session_state.selected_answers[idx] = None

        # Safely render the radio buttons
        selected_option = st.session_state.selected_answers[idx]
        selected_index = options.index(selected_option) if selected_option in options else -1

        st.write(f"**{idx + 1}. {question}**")
        st.session_state.selected_answers[idx] = st.radio(
            f"Question {idx + 1}",
            options,
            index=selected_index,
            key=f"quiz_{idx}",
        )

    # Submit Button
    if st.button("Submit Quiz"):
        st.session_state.show_results = True

# Display Quiz Results
if st.session_state.show_results:
    st.subheader("Quiz Results")
    correct_answers = 0

    for idx, quiz in enumerate(st.session_state.quiz_data):
        question = quiz.get("Question", "No question available.")
        correct_answer = quiz.get("Correct Answer", "No correct answer provided.")
        explanation = quiz.get("Explanation", "No explanation provided.")
        user_answer = st.session_state.selected_answers[idx]

        st.write(f"**{idx + 1}. {question}**")
        st.write(f"- **Your Answer:** {user_answer}")
        st.write(f"- **Correct Answer:** {correct_answer}")

        if user_answer == correct_answer:
            st.success("Correct!")
            correct_answers += 1
        else:
            st.error("Incorrect.")
        st.info(f"**Explanation:** {explanation}")

    st.write(f"**Your Score: {correct_answers}/{len(st.session_state.quiz_data)}**")

# Ask a Doubt Button
with col3:
    doubt_query = st.text_input("Enter your doubt:", key="doubt_input")
    if st.button("Ask a Doubt"):
        with st.spinner("Processing your doubt..."):
            doubt_response = send_chat_request(selected_video_id, "Ask a Doubt", query=doubt_query)
            st.session_state.doubt_response = doubt_response

# Display Doubt Response
if st.session_state.doubt_response:
    st.subheader("Doubt Response")
    st.write(st.session_state.doubt_response)

st.markdown('</div>', unsafe_allow_html=True)
