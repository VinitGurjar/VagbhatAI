import streamlit as st
from llm_chain import load_normal_chain
from langchain.memory import StreamlitChatMessageHistory
import yaml
import os
with open("config.yaml","r") as f:
    config = yaml.safe_load(f)


#for llm chain
def load_chain(chat_history):
    return load_normal_chain(chat_history)

def clear_input_field():
    st.session_state.user_question = st.session_state.user_input
    st.session_state.user_input = ""

def set_send_input():
    st.session_state.send_input = True
    clear_input_field()

#main Client
def main():
    st.title("VAGBHAT AI")
    chat_container = st.container()
    st.sidebar.title("Chat Sessions")
    chat_sessions = ["new_session"] + os.listdir(config["chat_history_path"])

    #session state definitions
    if "send_input" not in st.session_state:
        st.session_state.send_input = False
        st.session_state.user_question = ""

    st.sidebar.selectbox("Select a chat session", chat_sessions, key="session_key")

    chat_history = StreamlitChatMessageHistory(key="history")
    llm_chain = load_chain(chat_history)

    user_input = st.text_input("Ask Query here", key="user_input", on_change=set_send_input)

    send_button = st.button("Send", key="send_button")

    if send_button or st.session_state.send_input:
        if st.session_state.user_question != "":


            with chat_container:
                st.chat_message("user").write(st.session_state.user_question)
                llm_response = llm_chain.run(st.session_state.user_question)
                st.session_state.user_question = ""

    if chat_history.messages !=[]:
        with chat_container:
            st.write("Chat History")
            for message in chat_history.messages:
                st.chat_message(message.type).write(message.content)

if __name__ == "__main__":
    main()