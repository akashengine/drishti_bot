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
    Handles multiple JSON objects within each string and proper Unicode handling.
    """
    try:
        raw_items = ast.literal_eval(raw_data)
        quiz_data = []
        for raw_item in raw_items:
            try:
                json_objects = raw_item.strip().split('\n\n')
                for json_obj in json_objects:
                    if not json_obj.strip():
                        continue
                    cleaned_item = json_obj.strip()
                    # Decode JSON string to ensure proper handling of Unicode text
                    cleaned_item = json.loads(cleaned_item)
                    quiz_data.append(cleaned_item)
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
        st.error(f"Raw data received: {raw_data[:200]}...")
        return None

# -------------------------------------------------------------
# Quiz-Related Functions
# -------------------------------------------------------------
def fetch_new_quiz():
    st.session_state.show_quiz = True
    with st.spinner("Fetching quiz..."):
        quiz_response = send_chat_request(st.session_state.video_id, "Quiz Me")
    if "Error" not in quiz_response:
        st.write("Debug: Raw API Response")
        with st.expander("Show raw response"):
            st.code(quiz_response)

        processed_data = preprocess_quiz_data(quiz_response)
        if processed_data:
            st.session_state.quiz_data = processed_data
            st.session_state.quiz_submitted = False
            if 'user_answers' in st.session_state:
                del st.session_state.user_answers

            st.write("Debug: Processed Quiz Data")
            with st.expander("Show processed data"):
                st.json(processed_data)
        else:
            st.error("Failed to process quiz data")
    else:
        st.error(quiz_response)

def render_quiz(quiz_data):
    """
    Renders the quiz dynamically based on the JSON response.
    """
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
            # Use 'hindi-text' class for Hindi rendering
            st.markdown(f'<div class="hindi-text">{question["Question"]}</div>', unsafe_allow_html=True)
            options = [
                question["Option 1"],
                question["Option 2"],
                question["Option 3"],
                question["Option 4"],
            ]

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
                st.markdown(f"<div class='hindi-text'>**Correct Answer:** {correct_answer_text}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='hindi-text'>**Explanation:** {question['Explanation']}</div>", unsafe_allow_html=True)
                st.markdown("---")

            score_percentage = (total_correct / len(quiz_data)) * 100
            st.markdown(f"### Final Score: {total_correct}/{len(quiz_data)} ({score_percentage:.1f}%)")

# -------------------------------------------------------------
# Streamlit App Layout
# -------------------------------------------------------------
st.set_page_config(page_title="DrishtiGPT", layout="wide")

# CSS for Hindi Font Styling
st.markdown("""
    <style>
    @font-face {
        font-family: 'NotoSansDevanagari';
        src: url('https://fonts.gstatic.com/s/notosansdevanagari/v14/4UaMrENHsxJlGDuGo1OIlL3xD9ZhCDN02-oGV0H-jHw.woff2') format('woff2');
    }
    .hindi-text {
        font-family: 'NotoSansDevanagari', sans-serif;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = None
if 'show_quiz' not in st.session_state:
    st.session_state.show_quiz = False

# Sidebar for Video Selection
st.sidebar.title("DrishtiGPT")
st.sidebar.markdown('<div class="sidebar">', unsafe_allow_html=True)

video_ids = ["7781", "11853", "160841"]
selected_video_id = st.sidebar.selectbox("Select Video ID", video_ids)
st.sidebar.markdown('</div>', unsafe_allow_html=True)
st.session_state.video_id = selected_video_id

# Main Content
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.markdown(f"""
    <div class="video-placeholder">
        <iframe 
            src="https://console.frontbencher.in/flm/video-player-iframe-OJ5fnQP8q7Z8X1EhbH7Fvthdc74vbfy9/{selected_video_id}"
            width="800"
            height="450"
            allowfullscreen
            allow="accelerometer; ambient-light-sensor; autoplay; battery; camera; clipboard-write; document-domain; encrypted-media; fullscreen; geolocation; gyroscope; layout-animations; legacy-image-formats; magnetometer; microphone; midi; oversized-images; payment; picture-in-picture; publickey-credentials-get; sync-xhr; usb; vr ; wake-lock; xr-spatial-tracking"
            sandbox="allow-forms allow-modals allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts allow-downloads"
        ></iframe>
    </div>
""", unsafe_allow_html=True)

# Action Buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Summary"):
        st.subheader("Video Summary")
        with st.spinner("Fetching summary..."):
            summary_response = send_chat_request(selected_video_id, "Summary")

        if "Error" not in summary_response:
            st.success("Summary fetched successfully!")
            st.markdown(summary_response)
        else:
            st.error(summary_response)

with col2:
    if st.button("Quiz Me"):
        fetch_new_quiz()

    if st.session_state.show_quiz and st.session_state.quiz_data:
        render_quiz(st.session_state.quiz_data)

with col3:
    if st.button("Ask a Doubt"):
        st.subheader("Ask a Doubt")
        dify_chat_html = f"""
            <iframe
                id="difyFrame"
                src="https://testing.drishtigpt.com/chat/xP5VTne5QOVw1EhE"
                width="100%"
                height="600px"
                frameborder="0"
                allow="accelerometer; ambient-light-sensor; autoplay; battery; camera; clipboard-write; document-domain; encrypted-media; fullscreen; geolocation; gyroscope; layout-animations; legacy-image-formats; magnetometer; microphone; midi; oversized-images; payment; picture-in-picture; publickey-credentials-get; sync-xhr; usb; vr ; wake-lock; xr-spatial-tracking"
                sandbox="allow-forms allow-modals allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts allow-downloads"
                style="border: 1px solid #ccc; border-radius: 8px;"
            ></iframe>
        """
        st.components.v1.html(dify_chat_html, height=650)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Developed by DrishtiGPT Team")
