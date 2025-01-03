import streamlit as st
import requests
import json

# API Configuration
API_BASE_URL = "https://testing.drishtigpt.com/v1/chat-messages"
API_KEY = st.secrets["API_KEY"]  # Securely retrieve API Key

# Initialize session state for quiz data
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = None

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
    Preprocesses raw quiz JSON string to convert it into a valid list of JSON objects.
    """
    try:
        # Split the string into individual JSON objects and wrap them in an array
        raw_data = raw_data.replace("\n", "").replace("}{", "},{")
        formatted_data = f"[{raw_data}]"
        quiz_data = json.loads(formatted_data)
        return quiz_data
    except Exception as e:
        st.error(f"Failed to preprocess quiz data: {e}")
        return None

def render_quiz(quiz_data):
    """
    Renders the quiz dynamically based on the JSON response.
    """
    if not quiz_data:
        st.error("No valid quiz data available.")
        return

    st.subheader("Quiz Me")
    
    # Initialize session state for user answers if not exists
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = [None] * len(quiz_data)
    
    # Initialize session state for quiz submission
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False

    for idx, question in enumerate(quiz_data, start=1):
        st.markdown(f"### {idx}. {question['Question']}")
        options = [
            question["Option 1"],
            question["Option 2"],
            question["Option 3"],
            question["Option 4"],
        ]
        
        # Use session state to store the selected answer
        answer_key = f"q_{idx}"
        if answer_key not in st.session_state:
            st.session_state[answer_key] = st.session_state.user_answers[idx-1]
            
        selected_answer = st.radio(
            f"Select your answer for Question {idx}:",
            options,
            key=answer_key,
        )
        st.session_state.user_answers[idx-1] = selected_answer

    if st.button("Submit Quiz"):
        st.session_state.quiz_submitted = True

    # Show results after submission
    if st.session_state.quiz_submitted:
        st.markdown("### Quiz Results")
        total_correct = 0
        
        for idx, (answer, question) in enumerate(zip(st.session_state.user_answers, quiz_data), start=1):
            is_correct = answer == question["Correct Answer"]
            if is_correct:
                total_correct += 1
                st.success(f"✅ Question {idx}: Correct")
            else:
                st.error(f"❌ Question {idx}: Incorrect")
            st.markdown(f"**Your Answer:** {answer}")
            st.markdown(f"**Correct Answer:** {question['Correct Answer']}")
            st.markdown(f"**Explanation:** {question['Explanation']}")
        
        # Display total score
        score_percentage = (total_correct / len(quiz_data)) * 100
        st.markdown(f"### Final Score: {total_correct}/{len(quiz_data)} ({score_percentage:.1f}%)")

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
    quiz_button = st.button("Quiz Me")
    if quiz_button:  # If Quiz Me button is clicked, reset and regenerate
        st.subheader("Quiz Me")
        with st.spinner("Fetching quiz..."):
            quiz_response = send_chat_request(selected_video_id, "Quiz Me")
        if "Error" not in quiz_response:
            st.session_state.quiz_data = preprocess_quiz_data(quiz_response)
            # Reset quiz state when loading new quiz
            st.session_state.quiz_submitted = False
            if 'user_answers' in st.session_state:
                del st.session_state.user_answers
        else:
            st.error(quiz_response)
    elif st.session_state.quiz_data is not None:  # Show existing quiz if available
        
        if st.session_state.quiz_data:
            render_quiz(st.session_state.quiz_data)

# Placeholder for Ask a Question
with col3:
    if st.button("Ask a Doubt"):
        st.subheader("Ask a Doubt")
        st.info("Ask Doubt functionality will be implemented here.")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Developed by DrishtiGPT Team")
