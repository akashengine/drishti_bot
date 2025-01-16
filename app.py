import streamlit as st
import requests
import json
import ast

# -------------------------------------------------------------
# API Configuration
# -------------------------------------------------------------
API_BASE_URL = "https://testing.drishtigpt.com/v1/chat-messages"
API_KEY = st.secrets["API_KEY"]  # Securely retrieve API Key

# -------------------------------------------------------------
# Helper Functions
# -------------------------------------------------------------
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

def preprocess_quiz_data(raw_data):
    """
    Preprocesses the quiz data from the API response into a list of dictionaries.
    Handles multiple JSON objects within each string and proper newline handling.
    """
    try:
        # Convert string representation of list to actual list using ast.literal_eval
        raw_items = ast.literal_eval(raw_data)
        
        # Parse each quiz item string into a dictionary
        quiz_data = []
        for raw_item in raw_items:
            try:
                json_objects = raw_item.strip().split('\n\n')
                for json_obj in json_objects:
                    if not json_obj.strip():
                        continue
                    cleaned_item = json_obj.strip()
                    cleaned_item = cleaned_item.encode().decode('unicode_escape')
                    quiz_dict = json.loads(cleaned_item)
                    quiz_data.append(quiz_dict)
            except json.JSONDecodeError as je:
                st.error(f"Failed to parse quiz item: {je}")
                st.error(f"Problematic item: {raw_item[:200]}...")
                continue
            
        if not quiz_data:
            st.error("No quiz questions could be parsed successfully")
            return None
            
        return quiz_data
    except Exception as e:
        st.error(f"Failed to preprocess quiz data: {str(e)}")
        st.error(f"Raw data received: {raw_data[:200]}...")  # Show first 200 chars for debugging
        return None

# -------------------------------------------------------------
# Streamlit App Layout
# -------------------------------------------------------------
st.set_page_config(page_title="DrishtiGPT", layout="wide")

# CSS for Hindi Font Styling
st.markdown("""
    <style>
    @font-face {
        font-family: 'HindiFont';
        src: url('https://fonts.gstatic.com/s/noto-sans-devanagari/v14/4UaMrENHsxJlGDuGo1OIlL3xD9ZhCDN02-oGV0H-jHw.woff2') format('woff2');
    }
    .hindi-text {
        font-family: 'HindiFont', sans-serif;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# Main Quiz Renderer
def render_quiz(quiz_data):
    if not quiz_data:
        st.error("No valid quiz data available.")
        return

    st.subheader("Quiz Me")
    st.info(f"Successfully loaded {len(quiz_data)} questions")

    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = [None] * len(quiz_data)

    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False

    quiz_container = st.container()
    with quiz_container:
        for idx, question in enumerate(quiz_data, start=1):
            st.markdown(f"### Question {idx}")
            # Render question text with Hindi font styling
            st.markdown(f'<div class="hindi-text">{question["Question"]}</div>', unsafe_allow_html=True)
            options = [question["Option 1"], question["Option 2"], question["Option 3"], question["Option 4"]]

            answer_key = f"q_{idx}"
            if answer_key not in st.session_state:
                st.session_state[answer_key] = st.session_state.user_answers[idx-1]

            selected_answer = st.radio(
                "Select your answer:",
                options,
                key=answer_key,
                index=None
            )
            st.session_state.user_answers[idx-1] = selected_answer
            st.markdown("---")

        if st.button("Submit Quiz"):
            st.session_state.quiz_submitted = True

        if st.session_state.quiz_submitted:
            st.markdown("### Quiz Results")
            total_correct = 0

            for idx, (answer, question) in enumerate(zip(st.session_state.user_answers, quiz_data), start=1):
                correct_answer = question["Correct Answer"]
                correct_answer_text = question[correct_answer]
                is_correct = answer == correct_answer_text

                if is_correct:
                    total_correct += 1
                    st.success(f"✅ Question {idx}: Correct")
                else:
                    st.error(f"❌ Question {idx}: Incorrect")

                st.markdown(f"**Your Answer:** {answer if answer else 'Not answered'}")
                st.markdown(f'<div class="hindi-text">**Correct Answer:** {correct_answer_text}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="hindi-text">**Explanation:** {question["Explanation"]}</div>', unsafe_allow_html=True)
                st.markdown("---")

            score_percentage = (total_correct / len(quiz_data)) * 100
            st.markdown(f"### Final Score: {total_correct}/{len(quiz_data)} ({score_percentage:.1f}%)")

# Add quiz fetch and rendering logic
if st.sidebar.button("Fetch Quiz"):
    fetch_new_quiz()
if st.session_state.quiz_data:
    render_quiz(st.session_state.quiz_data)
