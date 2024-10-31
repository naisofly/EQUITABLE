import os
import anthropic
import streamlit as st
import json
from enum import Enum
from typing import Dict, Optional

class ManagerStyle(Enum):
    SUPPORTIVE = "supportive"
    NEUTRAL = "neutral"
    RIGID = "rigid"

class NegotiationRoleplaySystem:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.system_prompt = """Our AI-powered negotiation training platform Promotes economic empowerment & leadership for women and girls, 
        one of the gender equity challenges outlined in UN SDG 5, by simulating real-world negotiation scenarios, 
        considering all the unconscious biases women face, providing a safe and interactive environment for women to practice and refine their skills. 
        By leveraging natural language processing and AI, the platform offers personalized feedback, suggests a customised strategic approach, 
        and highlights areas for improvement. It adapts to each user's skill level, ensuring that both beginners and experienced leaders can 
        benefit from tailored, practical training.

        As the manager in this roleplay, respond naturally in character without describing or explaining the manager's personality. 
        Keep responses focused on the conversation itself, as if it were a real workplace discussion."""
        self.conversation_history = []
        self.conversation_goal = None
        self.scenario_context = None
        self.current_manager = None

    def set_conversation_goal(self, goal: str, context: Dict):
            self.conversation_goal = goal
            self.scenario_context = context

    def get_manager_personality(self, style: ManagerStyle) -> Dict:
        print(f"Debug: Requested style: {style}")  # Add this line
        """Define manager personality based on selected style."""
        personalities = {
            ManagerStyle.SUPPORTIVE: {
                "name": "Sarah",
                "traits": """Empathetic and encouraging manager who believes in developing team members.
                           Prioritizes open communication and collaborative problem-solving.
                           Values work-life balance and employee growth.
                           More likely to support reasonable requests with proper justification."""
            },
            ManagerStyle.NEUTRAL: {
                "name": "Michael",
                "traits": """Balanced and objective manager focused on fairness and company policies.
                           Makes decisions based on both data and human factors.
                           Neither overly supportive nor overly rigid.
                           Considers both employee needs and business requirements equally."""
            },
            ManagerStyle.RIGID: {
                "name": "Laura",
                "traits": """Highly analytical and results-driven manager.
                           Challenging, no-nonsense, and impatient with vague requests.
                           Demands evidence and focuses on measurable outcomes.
                           More likely to say no unless completely convinced by data and justification."""
            }
        }
        self.current_manager = personalities.get(style)
        print(f"Debug: Retrieved manager: {self.current_manager}")  # Add this line
        return self.current_manager

    def process_message(self, user_message: str, manager_style: ManagerStyle) -> str:
        """Process a single message in the conversation without feedback"""
        if not self.current_manager:
            self.get_manager_personality(manager_style)

        self.conversation_history.append({"role": "user", "content": user_message})

        response_prompt = f"""You are {self.current_manager['name']}, a manager with these traits: {self.current_manager['traits']}

        Stay completely in character and respond naturally to this employee message as part of an ongoing workplace conversation. 
        Do not describe yourself or your personality - just respond as the manager would in a real conversation.

        Conversation Goal: {self.conversation_goal}
        Scenario Context: {json.dumps(self.scenario_context)}
        Previous Messages: {json.dumps(self.conversation_history[:-1])}
        Employee's Message: {user_message}"""

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0.7,
            system=self.system_prompt,
            messages=[
                {"role": "user", "content": response_prompt}
            ]
        )

        manager_response = response.content[0].text
        self.conversation_history.append({"role": "assistant", "content": manager_response})
        return manager_response

    def generate_final_feedback(self) -> Dict:
        """Generate comprehensive feedback for the entire conversation"""
        feedback_prompt = f"""Analyze this complete negotiation conversation:
        Goal: {self.conversation_goal}
        Context: {json.dumps(self.scenario_context)}
        Full Conversation History: {json.dumps(self.conversation_history)}

        Provide a comprehensive analysis and respond with a JSON object containing exactly these fields:
        {{
            "metrics": {{
                "effectiveness": {{ "score": <1-10>, "description": "<explanation>" }},
                "preparedness": {{ "score": <1-10>, "description": "<explanation>" }},
                "assertiveness": {{ "score": <1-10>, "description": "<explanation>" }},
                "confidence": {{ "score": <1-10>, "description": "<explanation>" }},
                "flexibility": {{ "score": <1-10>, "description": "<explanation>" }}
            }},
            "highlights": [
                "highlight1",
                "highlight2",
                ...
            ],
            "improvements": [
                "improvement1",
                "improvement2",
                ...
            ],
            "next_steps": [
                "step1",
                "step2",
                ...
            ]
        }}"""

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            temperature=0.7,
            system=self.system_prompt,
            messages=[
                {"role": "user", "content": feedback_prompt}
            ]
        )
        
        try:
            return json.loads(response.content[0].text)
        except json.JSONDecodeError:
            return {
                "metrics": {
                    "effectiveness": {"score": 0, "description": "Error generating feedback"},
                    "preparedness": {"score": 0, "description": "Error generating feedback"},
                    "assertiveness": {"score": 0, "description": "Error generating feedback"},
                    "confidence": {"score": 0, "description": "Error generating feedback"},
                    "flexibility": {"score": 0, "description": "Error generating feedback"}
                },
                "highlights": ["Error generating feedback"],
                "improvements": ["Error generating feedback"],
                "next_steps": ["Error generating feedback"]
            }
    
 

# Streamlit App
st.title("EQUITABLE")
st.caption("Empowering women to claim an equal seat at the table by mirroring gendered dynamics in the real world.")

# Initialize session state with default values
if "negotiation_system" not in st.session_state:
    api_key = "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"
    st.session_state.negotiation_system = NegotiationRoleplaySystem(api_key)
    st.session_state.current_style = ManagerStyle.NEUTRAL
    st.session_state.conversation_started = False
    st.session_state.messages = []
    st.session_state.feedback_generated = False

# Enhanced sidebar for manager selection with preview
with st.sidebar:
    st.header("Scenario Settings")
    
    # Manager style selection with preview
    st.subheader("Select Your Manager")
    manager_style = st.selectbox(
        "Manager Personality",
        [style.value for style in ManagerStyle],
        index=[style.value for style in ManagerStyle].index(st.session_state.current_style.value),
        help="Choose the type of manager you want to practice negotiating with"
    )
    
    # Preview section
    st.markdown("---")
    st.markdown("### Manager Preview")
    
    # Get current manager details
    current_manager = st.session_state.negotiation_system.get_manager_personality(ManagerStyle(manager_style))
    # Check if Manager Style is Selected & Display manager details in an organized way
    if current_manager:
        st.markdown(f"**Name:** {current_manager['name']}")
        st.markdown("**Management Style:**")
        for trait in current_manager['traits'].split('\n'):
            if trait.strip():
                st.markdown(f"- {trait.strip()}")
    else:
        st.error("Failed to load manager details. Please try selecting a different manager style.")
        
    
    # # Display manager details in an organized way
    # st.markdown(f"**Name:** {current_manager['name']}")
    # st.markdown("**Management Style:**")
    # for trait in current_manager['traits'].split('\n'):
    #     if trait.strip():
    #         st.markdown(f"- {trait.strip()}")
            
    # Add a confirmation button for personality change
    if st.button("Confirm Manager Selection"):
        if ManagerStyle(manager_style) != st.session_state.current_style:
            st.session_state.current_style = ManagerStyle(manager_style)
            st.session_state.conversation_started = False
            st.session_state.messages = []
            st.session_state.feedback_generated = False
            st.session_state.negotiation_system.conversation_history = []
            st.success(f"Manager changed to {current_manager['name']}! Conversation reset.")
            st.experimental_rerun()

# Main conversation area
if not st.session_state.conversation_started:
    # Display initial scenario setup
    st.info(f"""
    🎯 **Negotiation Scenario Setup**
    - Your Manager: {current_manager['name']} ({manager_style})
    - Goal: Convince your manager to invest in your professional development training
    - Location: Local training next month
    
    Type your message below to start the conversation...
    """)
    
    st.session_state.negotiation_system.set_conversation_goal(
        "Convince manager to invest in training next month",
        {
            "training_type": "professional development",
            "timeline": "next month",
            "location": "local",
            "manager_style": manager_style
        }
    )
    st.session_state.conversation_started = True

# Display conversation history
for message in st.session_state.negotiation_system.conversation_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input with character counter
MAX_CHARS = 500
if prompt := st.chat_input(f"Your response... (max {MAX_CHARS} characters)", max_chars=MAX_CHARS):
    # Process and display messages
    response = st.session_state.negotiation_system.process_message(
        prompt, 
        st.session_state.current_style
    )
    
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        st.markdown(response)

# Feedback section
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Generate Feedback") and not st.session_state.feedback_generated:
        feedback = st.session_state.negotiation_system.generate_final_feedback()
        
        st.markdown("### Feedback Summary")
        
        # Display metrics in a more visual way
        st.markdown("#### Performance Metrics")
        cols = st.columns(5)
        for i, (metric, data) in enumerate(feedback["metrics"].items()):
            with cols[i]:
                # Create a more visual metric display
                score = data['score']
                color = 'green' if score >= 7 else 'orange' if score >= 4 else 'red'
                st.markdown(f"""
                    <div style='text-align: center'>
                        <h4>{metric.title()}</h4>
                        <h2 style='color: {color}'>{score}/10</h2>
                        <p>{data['description']}</p>
                    </div>
                """, unsafe_allow_html=True)
        
        # Display other feedback sections
        for section in ['highlights', 'improvements', 'next_steps']:
            st.markdown(f"#### {section.replace('_', ' ').title()}")
            for item in feedback[section]:
                st.markdown(f"- {item}")
        
        st.session_state.feedback_generated = True

with col2:
    if st.button("Reset Conversation"):
        st.session_state.conversation_started = False
        st.session_state.messages = []
        st.session_state.feedback_generated = False
        st.session_state.negotiation_system.conversation_history = []
        st.success("Conversation reset! Select a manager style to start again.")
        st.experimental_rerun()