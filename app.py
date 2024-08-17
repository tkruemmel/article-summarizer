import streamlit as st
from langchain_community.llms import Ollama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from validators import url as validate_url
from kgk_controller import find_specific_post
from lxml import html


def remove_html_from_string(html_string):
    tree = html.fromstring(html_string)
    text = tree.text_content()
    return text


llm = Ollama(
    model="phi:latest", base_url="http://ollama-container:11434", verbose=True
)


def sendPrompt(prompt):
    global llm
    response = llm.invoke(prompt)
    return response


# raise Exception("THIS IS NIKOLE:", prompt, validate_url(prompt))
# Exception: ('THIS IS NIKOLE:', 'whats your favorite color?', ValidationError(func=url, args={'value': 'whats your favorite color?'}))

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

        content = remove_html_from_string(content['content']['rendered'])
        user_message["llmContent"] = (
            f"Bitte schreiben Sie eine Zusammenfassung des folgenden Textes:\n\n{content}"
        )
    except AssertionError as err:
        user_message["error"] = str(err)
    st.session_state.messages.append(user_message)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Ein Moment..."):
            response = st.session_state.messages[-1].get("error") or sendPrompt(
                st.session_state.messages[-1]["llmContent"]
            )
            st.write(response)
            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )
