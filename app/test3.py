import anthropic
import streamlit as st
from streamlit_option_menu import option_menu
from typing import List


# Display the horizontal menu bar
selected = option_menu(
    menu_title=None,
    options=["Let's Roleplay", "Progress", "About Equitable"],
    orientation="horizontal"
)

# Display the content based on the selected option
if selected == "Let's Roleplay":
    st.title("Let's Roleplay")
    
    # Inputs for manager's personality, scenario, and goal
    manager_personality = st.selectbox("Select your manager's personality:", ["Select...", "Supportive", "Neutral", "Rigid"])
    benefit_scenario = st.text_input("Describe the benefit scenario:")
    goal = st.text_input("What is your goal?")
    
    # Add the "Start Roleplay" button
    start_roleplay = st.button("Start Roleplay")
    
    # Add logic for starting the roleplay if needed
    if start_roleplay and manager_personality != "Select..." and benefit_scenario and goal:
        st.write("Roleplay scenario initialized with:")
        st.write(f"Manager's personality: {manager_personality}")
        st.write(f"Benefit scenario: {benefit_scenario}")
        st.write(f"Goal: {goal}")
        
        # Display the chat interface below inputs (add your chat implementation here)

elif selected == "Progress":
    st.title("Your Progress")
    st.write("Display user's progress and metrics here.")

elif selected == "About Equitable":
    st.title("About Equitable")
    st.write("""
    **EQUITABLE** is an AI-powered negotiation training platform dedicated to promoting economic empowerment 
    and leadership for women and girls. Our platform simulates real-world negotiation scenarios, considering all the unconscious 
    biases, microaggressions, and gendered dynamics women face. We provide a safe and interactive environment for women to practice 
    and refine their negotiation skills.
    
    By leveraging natural language processing and AI, EQUITABLE offers personalized feedback, suggests a customized strategic approach, 
    and highlights areas for improvement. Our goal is to adapt to each user's skill level, ensuring that both beginners and experienced leaders 
    can benefit from tailored, practical training.
    """)

# Path to the logo image
logo_path = r"C:\Users\tejas\EQUITABLE\image\image.png"

# Display the logo in the sidebar with a specific width to control size
st.sidebar.image(logo_path, width=200)

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

# Select Manager's Personality
manager_personality = st.sidebar.selectbox("Select your manager's personality:", ["Select...","Supportive", "Neutral", "Rigid"])
benefit_scenario = st.sidebar.text_input("Describe the benefit scenario:")
goal = st.sidebar.text_input("What is your goal?")

# Add the "Let's Roleplay" button
start_roleplay = st.sidebar.button("Let's Roleplay")



# Initialize the chat history if it doesn't exist
if start_roleplay and "messages" not in st.session_state and manager_personality != "Select..." and benefit_scenario and goal :
    st.session_state.messages = []

    
    
    # Add the initial prompt
    initial_prompt = f"""I'm a woman and I need to roleplay a benefits negotiation scenario.

        
        My manager is {manager_personality.lower()}.
        My scenario: {benefit_scenario.lower()}
        My goal is to {goal.lower()}.

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

# Function to handle submission
def submit():
    # Store the input in messages and clear the input field
    st.session_state.messages.append({"role": "user", "content": st.session_state.user_input})
    st.session_state.user_input = ""  # Clear the input after submission

    # Generate AI's response
    ai_response = generate_response([{"role": m["role"], "content": m["content"]} for m in st.session_state.messages])
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

# Display the chat history
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create placeholders for user input and AI response
user_message_placeholder = st.empty()
ai_response_placeholder = st.empty()

# Text input for user message with on_change callback to submit
st.text_input("Enter your message here:", key="user_input", on_change=submit)
