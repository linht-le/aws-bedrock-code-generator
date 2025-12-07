import requests
import streamlit as st

API_URL = "http://localhost:8000/chat"

st.set_page_config(page_title="Code Generation Chatbot", page_icon="💻")
st.title("💻 Code Generation Chatbot")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        content = msg["content"]

        # Display code highlight
        if "```" in content:
            parts = content.split("```")
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    if part.strip():
                        st.write(part)
                else:
                    lines = part.split("\n", 1)
                    if len(lines) == 2:
                        lang, code = lines
                        st.code(code, language=lang.strip())
                    else:
                        st.code(part)
        else:
            st.write(content)

# Chat input
user_input = st.chat_input("Your message:")
if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message immediately
    with st.chat_message("user"):
        st.write(user_input)

    # Display assistant response with spinner
    with st.chat_message("assistant"), st.spinner("Generating code..."):
        payload = {"messages": st.session_state.messages}
        try:
            resp = requests.post(API_URL, json=payload, timeout=60).json()

            if resp.get("success") and resp.get("response"):
                response_content = resp["response"]
                st.session_state.messages.append({"role": "assistant", "content": response_content})

                # Display response
                if "```" in response_content:
                    parts = response_content.split("```")
                    for i, part in enumerate(parts):
                        if i % 2 == 0:
                            if part.strip():
                                st.write(part)
                        else:
                            lines = part.split("\n", 1)
                            if len(lines) == 2:
                                lang, code = lines
                                st.code(code, language=lang.strip())
                            else:
                                st.code(part)
                else:
                    st.write(response_content)
            else:
                error_msg = f"Error: {resp.get('error', 'Unknown error')}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

        except requests.exceptions.Timeout:
            error_msg = "Request timeout. Please try again."
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
        except Exception as e:
            error_msg = f"Failed to call API: {str(e)}"
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

    # Force rerun to show new messages
    st.rerun()
