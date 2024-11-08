import anthropic
import streamlit as st
from google.cloud import speech
from typing import List
from elevenlabs import play
from elevenlabs.client import ElevenLabs
import re

# Path to the logo image
logo_path = r"C:\Users\tejas\EQUITABLE\image\logo.png"
st.logo(logo_path,size="large")

# Set up the Streamlit page title and caption
st.title("EQUITABLE")
st.caption("Empowering women to claim an equal seat at the table by mirroring gendered dynamics in the real world.")

# Define constants
AI_MODEL = "claude-3-5-sonnet-20241022"
ANTHROPIC_API_KEY = "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"
ELEVENLABS_API_KEY = "sk_7475c8a88842abfa6ff5ae672b13517ad1a93bdb53199bd4"
SYSTEM_PROMPT = """Our AI-powered negotiation training platform Promotes economic empowerment & leadership for women and girls, 
one of the gender equity challenges outlined in UN SDG 5, by simulating real-world negotiation scenarios, considering all the 
unconscious biases, microaggressions, gendered dynamics women face, providing a safe and interactive environment for women to 
practice and refine their skills. By leveraging natural language processing and AI, the platform offers personalized feedback, 
suggests a customised strategic approach, and highlights areas for improvement. It adapts to each user's skill level, ensuring 
that both beginners and experienced leaders can benefit from tailored, practical training."""

# Initialize the Anthropic client
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Initialize Google Speech client
speech_client = speech.SpeechClient()

# Initialize ElevenLabs client
eleven_labs = ElevenLabs(api_key=ELEVENLABS_API_KEY)

#inputs for user configuration
manager_personality = st.selectbox("Select your manager's personality:", ["Select...", "Supportive", "Neutral", "Rigid"])
benefit_scenario = st.text_input("Describe the benefit scenario:")
goal = st.text_input("What is your goal?")

# Add the "Let's Roleplay" button
start_roleplay = st.button("Let's Roleplay")


# Function to generate AI response
def generate_response(messages):
    with client.messages.stream(max_tokens=1024, system=SYSTEM_PROMPT, messages=messages, model=AI_MODEL) as stream:
        return "".join([str(text) if text is not None else "" for text in stream.text_stream])

# Function to Transcribe audio using Google Speech-to-Text API and format the results.
def transcribe_audio(audio_bytes: bytes) -> str:
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )
    response = speech_client.recognize(config=config, audio=audio)
    formatted_transcripts = [result.alternatives[0].transcript.strip() for result in response.results if result.alternatives]
    return "\n".join(formatted_transcripts)

# Function to extract manager's dialogue
def extract_manager_dialogue(text):
    # Look for text within quotes, which should be the manager's dialogue
    manager_lines = re.findall(r'"([^"]*)"', text)
    return " ".join(manager_lines)

# Function to generate and play audio
def generate_and_play_audio(text):
    if text:  # Only generate and play audio if there's text to speak
        audio = eleven_labs.generate(
            text=text,
            voice="Eric",
            model="eleven_multilingual_v2"
        )
        play(audio)

## Start roleplay only when the button is clicked
if start_roleplay:
    # Initialize the chat history if not done already
    if not st.session_state.messages:
    
     initial_prompt = """I'm a woman and I need to roleplay a benefits negotiation scenario.
        My goal is to approve my leave request.
        My manager is neutral/professional. Put all manager responses in quotes.
        After the roleplay scenario, I want a Feedback Summary with highlights with actionable next steps after the conversation using a 10 point scale for the below metrics:
        * Effectiveness (Did you meet your goal?)
        * Preparedness (Have you done your research?)
        * Assertiveness
        * Confidence
        * Flexibility (Can you reach a reasonable compromise or a middle ground?)"""

    st.session_state.messages.append({"role": "user", "content": initial_prompt})
    
    initial_response = generate_response([{"role": "user", "content": initial_prompt}])
    st.session_state.messages.append({"role": "assistant", "content": initial_response})
    
    manager_dialogue = extract_manager_dialogue(initial_response)
    generate_and_play_audio(manager_dialogue)

# Display the chat history
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create placeholders for user input and AI response
user_message_placeholder = st.empty()
ai_response_placeholder = st.empty()

# Always display the audio input widget
audio_input = st.experimental_audio_input("Say something")

# Main Loop
if audio_input is not None:
    audio_bytes = audio_input.read()
    transcribed_text = transcribe_audio(audio_bytes)

    if transcribed_text:
        st.session_state.messages.append({"role": "user", "content": transcribed_text})
        with user_message_placeholder.chat_message("user"):
            st.markdown(transcribed_text)

        with ai_response_placeholder.chat_message("assistant"):
            full_response = generate_response([{"role": m["role"], "content": m["content"]} for m in st.session_state.messages])
            st.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        manager_dialogue = extract_manager_dialogue(full_response)
        if manager_dialogue:
            generate_and_play_audio(manager_dialogue)