import copy
import os

from langchain_community.document_loaders import TextLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema.document import Document
from langchain_together import Together

from custom_max_token_llm import CustomMaxTokenLLM


TOGETHER_API_KEY = os.environ.get('TOGETHER_API_KEY', 'KEY')


# define multiple prompts
PROMPTS = [
    '''Schreiben Sie eine Zusammenfassung des folgenden Textes mit maximal 864 Token:

    {text}

    ZUSAMMENFASSUNG:''',
    '''Erstellen Sie eine prägnante und umfassende Zusammenfassung des bereitgestellten Artikels mit einer maximalen Länge von 864 Tokens. Halten Sie sich an folgende Richtlinien:

Erstellen Sie eine Zusammenfassung, die detailliert, gründlich, ausführlich und komplex ist und dabei Klarheit und Prägnanz behält.

Integrieren Sie Hauptgedanken und wesentliche Informationen, entfernen Sie überflüssige Inhalte und konzentrieren Sie sich auf zentrale Aspekte.

Verlassen Sie sich strikt auf den bereitgestellten Text, ohne Einbeziehung externer Informationen:

    {text}

    ZUSAMMENFASSUNG:''',
    '''Schreiben Sie eine Zusammenfassung des folgenden Textes mit einer maximalen Länge von 864 Tokens. Schreiben Sie die Zusammenfassung so, dass sie ein Kleinkind verstehen würde:

    {text}

    ZUSAMMENFASSUNG:''',
]


# load a document using langchain's TextLoader
def load_data(doc):
    loader = TextLoader(doc)
    data = loader.load()
    return data


# save summary to txt file
def save_summary(summary):
    with open('summary.txt', 'w+') as file:
        file.writelines(summary)


# split content into chunks
def get_text_chunks_langchain(text):
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = [Document(page_content=x) for x in text_splitter.split_text(text)]
    return docs


# generate summary from given content based on the chosen prompt(s)
def summarize(loaded_text, promp_index=None):
    max_tokens = 864

    # Initialize the base language model
    base_llm = Together(
        model='mistralai/Mixtral-8x22B-Instruct-v0.1',
        together_api_key=TOGETHER_API_KEY,
        max_tokens=3500,  # Set the max_tokens value here
    )

    custom_llm = CustomMaxTokenLLM(llm=base_llm, max_tokens=max_tokens)

    # if prompt_index is specified and a valid index of available prompts,
    # generate summary using only that prompt, otherwise use all
    prompts = copy.copy(
        PROMPTS
        if promp_index is None or promp_index not in range(0, len(PROMPTS))
        else [PROMPTS[promp_index]]
    )

    # process each prompt and store the output in the appropriate column
    for i, prompt in enumerate(prompts):
        prompt_template = PromptTemplate(
            template=prompt, input_variables=['text']
        )

        # define the summarization chain for the current prompt
        chain = load_summarize_chain(
            custom_llm, chain_type='stuff', prompt=prompt_template, verbose=True
        )

        # generate the summary for the current prompt
        summary = chain.invoke(loaded_text)
        output = summary['output_text']
        print(f'Prompt {i+1} Summary: {output}')

    # return last generated summary
    return output
