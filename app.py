import streamlit as st
import requests
import json

# API Configuration
API_BASE_URL = "https://testing.drishtigpt.com/v1/chat-messages"
API_KEY = st.secrets["API_KEY"]


def send_chat_request(video_id, request_type, query="."):
    """
    Sends a request to the chat API with the given parameters.
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
        "user": "abc-123",
    }
    response = requests.post(API_BASE_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json().get("answer", "No response available.")
    else:
        return f"Error: {response.status_code} - {response.json().get('message', response.text)}"


def parse_quiz_data(raw_data):
    """
    Safely parse quiz data from JSON or raw string.
    """
    try:
        quizzes = []
        for quiz in raw_data.strip().split("\n\n"):
            quizzes.append(json.loads(quiz))
        return quizzes
    except Exception as e:
        st.error(f"Failed to parse quiz data: {e}")
        return []


# App Layout
st.set_page_config(page_title="DrishtiGPT Quiz", layout="wide")
st.title("DrishtiGPT")

# Sidebar for Video Selection
video_ids = ["7781", "7782", "7783"]  # Dummy Video IDs
selected_video_id = st.sidebar.selectbox("Select Video ID", video_ids)

# Load quiz state
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = []
if "selected_answers" not in st.session_state:
    st.session_state.selected_answers = {}
if "show_results" not in st.session_state:
    st.session_state.show_results = False


# Fetch Quiz Data
if st.button("Fetch Quiz"):
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

        # Render question and options
        st.write(f"**{idx + 1}. {question}**")
        st.session_state.selected_answers[idx] = st.radio(
            f"Select an option for question {idx + 1}:",
            options,
            index=options.index(st.session_state.selected_answers[idx])
            if st.session_state.selected_answers[idx] in options
            else -1,
            key=f"quiz_{idx}",
        )

    # Submit Button
    if st.button("Submit Quiz"):
        st.session_state.show_results = True

# Display Results
if st.session_state.show_results:
    st.subheader("Quiz Results")
    correct_answers = 0

    for idx, quiz in enumerate(st.session_state.quiz_data):
        question = quiz.get("Question", "No question available.")
        correct_answer = quiz.get("Correct Answer", "No correct answer provided.")
        explanation = quiz.get("Explanation", "No explanation provided.")

        st.write(f"**{idx + 1}. {question}**")
        st.write(f"- **Your Answer:** {st.session_state.selected_answers[idx]}")
        st.write(f"- **Correct Answer:** {correct_answer}")

        if st.session_state.selected_answers[idx] == correct_answer:
            st.success("Correct!")
            correct_answers += 1
        else:
            st.error("Incorrect.")
        st.info(f"**Explanation:** {explanation}")

    st.write(f"**Your Score: {correct_answers}/{len(st.session_state.quiz_data)}**")
