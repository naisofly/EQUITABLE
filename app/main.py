import os
import anthropic
import streamlit as st

st.title("EQUITABLE")
st.caption("Empowering women to claim an equal seat at the table by mirroring gendered dynamics in the real world.")

ai_model = "claude-3-5-sonnet-20241022"
api_key = "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"

client = anthropic.Anthropic(
    api_key=api_key,
)

if "ai_model" not in st.session_state:
    st.session_state["ai_model"] = ai_model

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

    st.session_state.messages.append({"role": "user", "content": initial_prompt})
    
    # Generate AI response for the initial prompt
    with client.messages.stream(
        max_tokens=1024,
        system="Our AI-powered negotiation training platform Promotes economic empowerment & leadership for women and girls, one of the gender equity challenges outlined in UN SDG 5, by simulating real-world negotiation scenarios, considering all the unconscious biases, microaggressions, gendered dynamics women face, providing a safe and interactive environment for women to practice and refine their skills. By leveraging natural language processing and AI, the platform offers personalized feedback, suggests a customised strategic approach, and highlights areas for improvement. It adapts to each user's skill level, ensuring that both beginners and experienced leaders can benefit from tailored, practical training.\n",
        messages=[{"role": "user", "content": initial_prompt}],
        model=st.session_state["ai_model"],
    ) as stream:
        full_response = "".join([str(text) if text is not None else "" for text in stream.text_stream])
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Display messages
for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        with client.messages.stream(
            max_tokens=1024,
            system="Our AI-powered negotiation training platform Promotes economic empowerment & leadership for women and girls, one of the gender equity challenges outlined in UN SDG 5, by simulating real-world negotiation scenarios, considering all the unconscious biases, microaggressions, gendered dynamics women face, providing a safe and interactive environment for women to practice and refine their skills. By leveraging natural language processing and AI, the platform offers personalized feedback, suggests a customised strategic approach, and highlights areas for improvement. It adapts to each user's skill level, ensuring that both beginners and experienced leaders can benefit from tailored, practical training.\n",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            model=st.session_state["ai_model"],
        ) as stream:
            for text in stream.text_stream:
                full_response += str(text) if text is not None else ""
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})