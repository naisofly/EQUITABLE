# Previously test2.py; To be edited  to retreive chat history from Google Firestore
import anthropic
import streamlit as st
import time
from typing import List

# Path to the logo image
logo_path = r"image\logo.png"

# Display logo 
st.logo(logo_path, size="large")

# Set up the Streamlit page title and caption
st.title("EQUITABLE")
st.caption("Goal: Secure a raise")

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

# Initialize session state for messages if not already done
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar inputs for user configuration
manager_personality = st.selectbox("Select your manager's personality:", ["Select...", "Supportive", "Neutral", "Rigid"])
benefit_scenario = st.text_input("Describe the benefit scenario:")
goal = st.text_input("What is your goal?")

# Add the "Let's Roleplay" button
start_roleplay = st.button("Let's Roleplay")

# Function to generate AI response
def generate_response(messages, include_feedback=False):
    system_prompt = SYSTEM_PROMPT
    # Modify the prompt to exclude feedback unless explicitly requested
    if not include_feedback:
        system_prompt += "\nNOTE: Do not generate feedback unless explicitly prompted."

    with client.messages.stream(max_tokens=1024, system=system_prompt, messages=messages, model=AI_MODEL) as stream:
        return "".join([str(text) if text is not None else "" for text in stream.text_stream])

# Start roleplay only when the button is clicked
if start_roleplay:
    # Initialize the chat history if not done already
    if not st.session_state.messages:
        initial_prompt = f"""I'm a woman named Sarah and I need to roleplay a benefits negotiation scenario.

        My manager is {manager_personality.lower()}.
        My scenario: {benefit_scenario.lower()}
        My goal is to {goal.lower()}.

        After the roleplay scenario, I want a Feedback Summary with highlights and actionable next steps after the conversation using a 10-point scale for the below metrics:
        * Effectiveness (Did you meet your goal?)
        * Preparedness (Have you done your research?)
        * Assertiveness
        * Confidence
        * Flexibility (Can you reach a reasonable compromise or a middle ground?)"""

        # Add user's initial prompt to the chat history
        st.session_state.messages.append({"role": "user", "content": initial_prompt})
        response = generate_response([{"role": "user", "content": initial_prompt}])
        st.session_state.messages.append({"role": "assistant", "content": response})

# Display the chat history and input box only if the roleplay has started
if st.session_state.messages:
    # Display the chat history
    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Function to handle submission
    def submit():
        # Store the input in messages and clear the input field
        st.session_state.messages.append({"role": "user", "content": st.session_state.user_input})
        st.session_state.user_input = ""  # Clear the input after submission

        # Generate AI's response
        ai_response = generate_response([{"role": m["role"], "content": m["content"]} for m in st.session_state.messages])
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

    # Create a text input for user interaction with on_change callback
    st.text_input("Enter your message here:", key="user_input", on_change=submit)

    # Add "Generate Feedback" button
    generate_feedback = st.button("Generate Feedback")

    if generate_feedback:
        feedback_response = generate_response([{"role": m["role"], "content": m["content"]} for m in st.session_state.messages], include_feedback=True)
        st.session_state.messages.append({"role": "assistant", "content": feedback_response})

        # Display the feedback with progress bars
        st.markdown("### Feedback Summary:")
        progress_text = "Generating feedback scores. Please wait."
        my_bar = st.progress(0, text=progress_text)

        # Simulate progress for loading
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        
        # Parse and display scores in the feedback response
        metrics = ["Effectiveness", "Preparedness", "Assertiveness", "Confidence", "Flexibility"]
        for metric in metrics:
            if metric in feedback_response:
                try:
                    # Extract the score (e.g., "Effectiveness: 8/10" -> 8)
                    score = int(feedback_response.split(f"{metric}: ")[1].split("/")[0].strip())
                    st.markdown(f"**{metric}:**")
                    st.progress(score / 10)  # Normalize the score to a 0-1 scale for the progress bar
                except (IndexError, ValueError):
                    continue

        time.sleep(1)
        my_bar.empty()
        st.markdown(feedback_response)
