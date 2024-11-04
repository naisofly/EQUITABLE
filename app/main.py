import anthropic
import streamlit as st
from google.cloud import speech
from typing import List

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

# Initialize Google Speech client
speech_client = speech.SpeechClient()

# Function to generate AI response
def generate_response(messages):
    with client.messages.stream(max_tokens=1024, system=SYSTEM_PROMPT, messages=messages, model=AI_MODEL) as stream:
        return "".join([str(text) if text is not None else "" for text in stream.text_stream])

# Function to Transcribe audio using Google Speech-to-Text API and format the results.
def transcribe_audio(audio_bytes: bytes) -> str:

    # Initialize the speech client
    speech_client = speech.SpeechClient()

    # Create the RecognitionAudio object
    audio = speech.RecognitionAudio(content=audio_bytes)

    # Configure the recognition settings
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
        enable_automatic_punctuation=True,  # Add punctuation for better formatting
    )

    # Perform the transcription
    response = speech_client.recognize(config=config, audio=audio)

    # Process and format the results
    formatted_transcripts: List[str] = []
    for result in response.results:
        if result.alternatives:
            # Get the transcript with the highest confidence
            transcript = result.alternatives[0].transcript.strip()
            if transcript:
                formatted_transcripts.append(transcript)

    # Join the formatted transcripts with line breaks
    return "\n".join(formatted_transcripts)

# Initialize the chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []
    
    # Add the initial prompt
    initial_prompt = """I'm a woman and I need to roleplay a benefits negotiation scenario.

        My goal is to approve my leave request.

        My manager is neutral/professional.

        After the roleplay scenario, I want a Feedback Summary with highlights with actionable next steps after the conversation using a 10 point scale for the below metrics:
        * Effectiveness (Did you meet your goal?)
        * Preparedness (Have you done your research?)
        * Assertiveness
        * Confidence
        * Flexibility (Can you reach a reasonable compromise or a middle ground?)"""

    # Add user's initial prompt to the chat history
    st.session_state.messages.append({"role": "user", "content": initial_prompt})
    
    # Generate and add AI's response to the initial prompt
    st.session_state.messages.append({"role": "assistant", "content": generate_response([{"role": "user", "content": initial_prompt}])})

# Display the chat history
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create placeholders for user input and AI response
user_message_placeholder = st.empty()
ai_response_placeholder = st.empty()

# Always display the audio input widget
audio_input = st.experimental_audio_input("Say something")

if audio_input is not None:
    # Transcribe audio to text
    audio_bytes = audio_input.read()
    transcribed_text = transcribe_audio(audio_bytes)

    if transcribed_text:
        # Add user's transcribed message to the chat history
        st.session_state.messages.append({"role": "user", "content": transcribed_text})
        with user_message_placeholder.chat_message("user"):
            st.markdown(transcribed_text)

        # Generate and display AI's response
        with ai_response_placeholder.chat_message("assistant"):
            full_response = generate_response([{"role": m["role"], "content": m["content"]} for m in st.session_state.messages])
            st.markdown(full_response)
        
        # Add AI's response to the chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})