import anthropic
import streamlit as st

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

# Function to generate AI response
def generate_response(messages):
    with client.messages.stream(max_tokens=1024, system=SYSTEM_PROMPT, messages=messages, model=AI_MODEL) as stream:
        return "".join([str(text) if text is not None else "" for text in stream.text_stream])

# Initialize the chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []
    
    # Add the initial prompt
    initial_prompt = """I'm a woman and I need to roleplay a benefits negotiation scenario.

        My goal is to convince my manager to invest in me attending a training next month in my city

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

# Display the chat history, starting after the first user prompt
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("What is up?"):
    # Add user's new message to the chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display AI's response
    with st.chat_message("assistant"):
        full_response = generate_response([{"role": m["role"], "content": m["content"]} for m in st.session_state.messages])
        st.markdown(full_response)
    
    # Add AI's response to the chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})