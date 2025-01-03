import streamlit as st
import requests

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
                "request_type": request_type,
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


def render_quiz(quiz_data):
    """
    Renders the quiz dynamically based on the JSON response.
    """
    if isinstance(quiz_data, str):
        try:
            quiz_data = eval(quiz_data)  # Convert JSON string to Python dictionary
        except Exception as e:
            st.error(f"Invalid quiz data format: {e}")
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
        user_answers.append({"user_answer": user_answer, "correct_answer": question["Correct Answer"], "explanation": question["Explanation"]})

    if st.button("Submit"):
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

# Sidebar for Video Selection
st.sidebar.title("DrishtiGPT")
video_ids = ["7781", "7782", "7783"]  # Dummy Video IDs
selected_video_id = st.sidebar.selectbox("Select Video ID", video_ids)

# Main Content
st.markdown(f"## Video Placeholder - Video ID: {selected_video_id}")

# Buttons for Actions
st.markdown("### Actions")

col1, col2, col3 = st.columns(3)

# Summary Button
with col1:
    if st.button("Summary"):
        st.subheader("Video Summary")
        with st.spinner("Fetching summary..."):
            summary_response = send_chat_request(selected_video_id, "Summary")
        if "Error" not in summary_response:
            st.success("Summary fetched successfully!")
            st.markdown(summary_response, unsafe_allow_html=True)
        else:
            st.error(summary_response)

# Quiz Me Button
with col2:
    if st.button("Quiz Me"):
        with st.spinner("Fetching quiz..."):
            quiz_response = send_chat_request(selected_video_id, "Quiz Me")
        if "Error" not in quiz_response:
            render_quiz(quiz_response)
        else:
            st.error(quiz_response)

# Ask a Doubt Button
with col3:
    if st.button("Ask a Doubt"):
        user_query = st.text_input("Ask your doubt here:")
        if st.button("Submit Doubt"):
            with st.spinner("Submitting your doubt..."):
                doubt_response = send_chat_request(selected_video_id, "Ask a Doubt", query=user_query)
            if "Error" not in doubt_response:
                st.success("Doubt submitted successfully!")
                st.markdown(doubt_response, unsafe_allow_html=True)
            else:
                st.error(doubt_response)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Developed by DrishtiGPT Team")
