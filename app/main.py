import os
import streamlit as st

from langchain_community.llms import Ollama
from lxml import html
from validators import url as validate_url

from summarizer import get_text_chunks_langchain, summarize
from kgk_controller import create_full_text, find_specific_post


LLM_HOME = os.environ.get('LLM_HOME', 'api_only')


# if the app is using the smaller locally downlowded llm initalize it
llm = (
    Ollama(
        model='phi:latest',
        base_url='http://ollama-container:11434',
        verbose=True,
    )
    if LLM_HOME == 'local_llm'
    # otherwise leave empty since LLM interaction will be handled by separate
    # api calls in summarize.py
    else None
)


# remove unnecessary html from kgk content for local llm use
def remove_html_from_string(html_string):
    tree = html.fromstring(html_string)
    text = tree.text_content()
    return text


# method to interact with the local llm
def send_prompt(prompt):
    global llm
    response = llm.invoke(prompt)
    return response


st.title('Article Summarizer')
# if no past messages in state add initial message
if 'messages' not in st.session_state.keys():
    st.session_state.messages = [
        {
            'role': 'assistant',
            'content': 'Bitte geben Sie eine URL an, die Sie zusammengefasst haben möchten.',
        }
    ]

# ask user for url input
if prompt := st.chat_input('Ihre URL'):
    user_message = {'role': 'user', 'content': prompt}
    try:
        # check validity of given url
        assert validate_url(prompt), 'Bitte geben Sie eine gültige URL an.'

        # find the apropriate kgk post
        content = find_specific_post(prompt)
        assert (  # check that content was retrieved properly
            content is not None
            and content.get('content', {}).get('rendered') is not None
        ), 'Der Inhalt der angegebenen URL konnte nicht abgerufen werden.'

        # format and send prompt/content off appropriately depending on if app
        # is using the local llm or not
        if LLM_HOME == 'local_llm':
            instruction = 'Bitte schreiben Sie eine Zusammenfassung des folgenden Textes:\n\n{}'
            user_message['llmContent'] = instruction.format(
                remove_html_from_string(content['content']['rendered'])
            )
        else:
            user_message['llmContent'] = get_text_chunks_langchain(
                create_full_text(content['content']['rendered'])
            )

    except AssertionError as err:
        # in case of an error add that to the state
        user_message['error'] = str(err)
    st.session_state.messages.append(user_message)

# have streamlit display message state for user
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])

# when the user has added a message, handle the content apropriately
if st.session_state.messages[-1]['role'] != 'assistant':
    with st.chat_message('assistant'):
        with st.spinner('Ein Moment...'):
            if st.session_state.messages[-1].get('error') == None:
                if LLM_HOME == 'local_llm':
                    response = send_prompt(
                        st.session_state.messages[-1]['llmContent']
                    )
                else:
                    response = summarize(
                        st.session_state.messages[-1]['llmContent'],
                        promp_index=0,
                    )
            else:
                response = st.session_state.messages[-1]['error']

            st.write(response)
            st.session_state.messages.append(
                {'role': 'assistant', 'content': response}
            )
