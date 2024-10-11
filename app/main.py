import streamlit as st
from validators import url as validate_url
from summarizer import get_text_chunks_langchain, summarize
from kgk_controller import create_full_text, find_specific_post
from lxml import html


st.title("Article Summarizer")
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Bitte geben Sie eine URL an, die Sie zusammengefasst haben möchten.",
        }
    ]

if prompt := st.chat_input("Ihre URL"):
    user_message = {"role": "user", "content": prompt}
    try:
        # check validity of given url
        assert validate_url(prompt), 'Bitte geben Sie eine gültige URL an.'

        content = find_specific_post(prompt)
        assert (  # check that content was retrieved properly
            content is not None
            and content.get('content', {}).get('rendered') is not None
        ), 'Der Inhalt der angegebenen URL konnte nicht abgerufen werden.'

        full_text = create_full_text(content['content']['rendered'])
        user_message["llmContent"] = get_text_chunks_langchain(full_text)
    except AssertionError as err:
        user_message["error"] = str(err)
    st.session_state.messages.append(user_message)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Ein Moment..."):
            response = st.session_state.messages[-1].get("error") or summarize(
                st.session_state.messages[-1]["llmContent"], promp_index=0
            )  # TODO: change prompt choice?
            st.write(response)
            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )
