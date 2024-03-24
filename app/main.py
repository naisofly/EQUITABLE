import os

import anthropic
import streamlit as st

st.title("Claude 3 by Streamlit")

ai_model = os.environ.get("AI_MODEL")
api_key = os.environ.get("API_KEY")

client = anthropic.Anthropic(
    api_key=api_key,
)
if "ai_model" not in st.session_state:
    st.session_state["ai_model"] = ai_model

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
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
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            model=st.session_state["ai_model"],
        ) as stream:
            for text in stream.text_stream:
                full_response += str(text) if text is not None else ""
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
