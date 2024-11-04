import anthropic
import streamlit as st
from google.cloud import speech
from typing import List, Dict

# Set up the Streamlit page title and caption
st.title("EQUITABLE")
st.caption("Empowering women to claim an equal seat at the table by mirroring gendered dynamics in the real world.")

# Define constants
AI_MODEL = "claude-3-5-sonnet-20241022"
API_KEY = "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"
SYSTEM_PROMPT = """Our AI-powered negotiation training platform Promotes economic empowerment & leadership for women and girls, 
one of the gender equity challenges outlined in UN SDG 5, by simulating real-world negotiation scenarios, considering all the 
unconscious biases, microaggressions, gendered dynamics women face, providing a safe and interactive environment for women to 
practice and refine their skills. By leveraging natural language processing and AI, the platform offers personalized feedback, 
suggests a customised strategic approach, and highlights areas for improvement. It adapts to each user's skill level, ensuring 
that both beginners and experienced leaders can benefit from tailored, practical training."""

# Initialize the Anthropic client
client = anthropic.Anthropic(api_key=API_KEY)

manager_personality = st.selectbox(
    "Choose your manager's personality:",
    ["Neutral", "Rigid", "Supportive"]
)

# Function to generate AI response
def generate_response(messages):
    with client.messages.stream(max_tokens=1024, system="", messages=messages, model=AI_MODEL) as stream:
        return "".join([str(text) if text is not None else "" for text in stream.text_stream])

# Function to parse and display feedback with progress bars
def display_feedback(feedback: str):
    # Define the metrics we are looking for
    metrics = ["Effectiveness", "Preparedness", "Assertiveness", "Confidence", "Flexibility"]
    feedback_lines = feedback.splitlines()
    scores: Dict[str, int] = {}

    # Parse feedback to extract scores
    for line in feedback_lines:
        for metric in metrics:
            if metric in line:
                try:
                    # Extract the score (e.g., "Effectiveness: 8/10" -> score 8)
                    score = int(line.split(":")[1].split("/")[0].strip())
                    scores[metric] = score
                except (IndexError, ValueError):
                    continue

    # Display colorful progress bars for each metric
    for metric, score in scores.items():
        st.markdown(f"**{metric}:**")
        st.progress(score / 10)  # Normalize to 0-1 scale for the progress bar


# Initialize the chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []
    initial_prompt = f"""I'm a woman and I need to roleplay a benefits negotiation scenario.

    My goal is to approve my leave request.

    My manager is {manager_personality.lower()}.

    After the roleplay scenario, I want a Feedback Summary with highlights and actionable next steps using a 10-point scale for:
    * Effectiveness (Did you meet your goal?)
    * Preparedness (Have you done your research?)
    * Assertiveness
    * Confidence
    * Flexibility (Can you reach a reasonable compromise or a middle ground?)"""

    st.session_state.messages.append({"role": "user", "content": initial_prompt})
    st.session_state.messages.append({"role": "assistant", "content": generate_response([{"role": "user", "content": initial_prompt}])})

# Display the chat history
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create placeholders for user input and AI response
user_message_placeholder = st.empty()
ai_response_placeholder = st.empty()

# Display a disabled audio input placeholder
st.text_input("Audio input (currently disabled)", disabled=True)

# Create a text input for user interaction
user_input = st.text_input("Enter your message:")

if user_input:
    # Add user's message to the chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with user_message_placeholder.chat_message("user"):
        st.markdown(user_input)

    # Generate and display AI's response
    with ai_response_placeholder.chat_message("assistant"):
        full_response = generate_response([{"role": m["role"], "content": m["content"]} for m in st.session_state.messages])
        st.markdown(full_response)

    # Add AI's response to the chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Display feedback with progress bars
    if "Feedback Summary" in full_response:
        display_feedback(full_response)