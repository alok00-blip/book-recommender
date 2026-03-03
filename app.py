
import streamlit as st
import vertexai
from vertexai.preview import reasoning_engines
import google.oauth2.service_account
import google.auth.transport.requests
import requests

PROJECT_ID = "book-recommender-488914"
LOCATION = "us-central1"
RESOURCE_NAME = "projects/118366759310/locations/us-central1/reasoningEngines/5429717171934593024"
SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

creds = google.oauth2.service_account.Credentials.from_service_account_info(
    dict(st.secrets),
    scopes=SCOPES
)

vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=creds)
agent = reasoning_engines.ReasoningEngine(RESOURCE_NAME)

st.title("📚 Book Recommender")
st.write("Tell me your mood or interests and I'll recommend the perfect book for you!")

if "session_id" not in st.session_state:
    session = agent.create_session(user_id="streamlit-user")
    st.session_state.session_id = session["id"]

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("E.g. I'm feeling stressed, suggest a book...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    with st.chat_message("assistant"):
        try:
            auth_req = google.auth.transport.requests.Request()
            creds.refresh(auth_req)
            url = f"https://us-central1-aiplatform.googleapis.com/v1/{RESOURCE_NAME}:streamQuery"
            headers = {
                "Authorization": f"Bearer {creds.token}",
                "Content-Type": "application/json"
            }
            payload = {
                "class_method": "stream_query",
                "input": {
                    "user_id": "streamlit-user",
                    "session_id": st.session_state.session_id,
                    "message": user_input
                }
            }
            response = requests.post(url, headers=headers, json=payload)
            data = response.json()
            response_text = ""
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and "content" in item:
                        for part in item["content"].get("parts", []):
                            if "text" in part:
                                response_text += part["text"]
            if not response_text:
                response_text = "Sorry I could not get a response. Please try again."
        except Exception as e:
            response_text = f"Error: {str(e)}"
        st.write(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})

