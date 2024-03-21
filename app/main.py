import os

import anthropic
import streamlit as st

ai_model = os.environ.get("AI_MODEL")
api_key = os.environ.get("API_KEY")

st.title("Craude 3 by Streamlit")

client = anthropic.Anthropic(
    api_key=api_key,
)
if "openai_model" not in st.session_state:
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
        stream = client.messages.create(
            max_tokens=1024,
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            model=st.session_state["ai_model"],
            stream=True,
        )
        if stream:
            for event in stream:
                response = ""
                match event.type:
                    case "message_start":
                        input_tokens = event.message.usage.input_tokens
                    case "content_block_start":
                        response = event.content_block.text
                    case "content_block_delta":
                        response = event.delta.text
                    case "message_delta":
                        output_tokens = event.usage.output_tokens

                full_response += str(response) if response is not None else ""
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
