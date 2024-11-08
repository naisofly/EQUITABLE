import anthropic
import streamlit as st
from google.cloud import speech
from typing import List, Dict

# Set up the Streamlit page title and caption
st.title("EQUITABLE")
st.caption("Empowering women to claim an equal seat at the table by mirroring gendered dynamics in the real world.")

#st.sidebar.image("logo.png", use_column_width=True) $can add once we finalize the logo

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

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #9370db; 
    }
    </style>
    """,
    unsafe_allow_html=True
)

manager_personality = st.sidebar.radio(
    "Choose your Manager's Personality:",
    ["Select a Personality","Neutral", "Rigid", "Supportive"]
)

# Function to change background color based on the selected manager personality
def set_background_color(personality):
    color_map = {
        "Neutral": "#D3D3D3",  # Light gray
        "Rigid": "#FFCCCC",    # Light red
        "Supportive": "#CCFFCC" # Light green
    }
    if personality in color_map:
        color = color_map[personality]
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-color: {color};
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

# Set the background color based on the selected personality
if manager_personality != "Select a Personality":
    set_background_color(manager_personality)

scenario_keyword=st.sidebar.text_input("Enter a keyword for the scenario (e.g. 'leave request')")

goal=st.sidebar.text_input("what is the goal of the conversation?")

# Function to generate AI response
def generate_response(messages):
    with client.messages.stream(max_tokens=1024, system="", messages=messages, model=AI_MODEL) as stream:
        return "".join([str(text) if text is not None else "" for text in stream.text_stream])


def display_feedback(feedback: str):
    # Define the metrics we are looking for
    metrics = ["Effectiveness", "Preparedness", "Assertiveness", "Confidence", "Flexibility"]
    feedback_lines = feedback.splitlines()
    scores: Dict[str, int] = {}

    # trying to display colorful progress bars for each metric here/not completely done
    for metric, score in scores.items():
        st.markdown(f"**{metric}:**")
        st.progress(score / 10)  # Normalize to 0-1 scale for the progress bar


# Initialize the chat history if it doesn't exist
if "messages" not in st.session_state and manager_personality != "Select a Personality":
    st.session_state.messages = []
    initial_prompt = f"""I'm a woman and I need to roleplay a benefits negotiation scenario.

    My scanario is {scenario_keyword}

    My goal is to {goal}

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