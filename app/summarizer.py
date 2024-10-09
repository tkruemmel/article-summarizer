import os

from langchain_community.document_loaders import TextLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema.document import Document
from langchain_together import Together

from custom_max_token_llm import CustomMaxTokenLLM


# ANYSCALE_API_BASE = os.environ["ANYSCALE_API_BASE"] = "https://api.endpoints.anyscale.com/v1"
# ANYSCALE_API_KEY = os.environ.get("ANYSCALE_API_KEY", "KEY")
TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY", "KEY")


def load_data(doc):
    loader = TextLoader(doc)
    data = loader.load()
    return data


def save_summary(summary):
    with open("summary.txt", "w+") as file:
        file.writelines(summary)


def get_text_chunks_langchain(text):
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = [Document(page_content=x) for x in text_splitter.split_text(text)]
    return docs


def summarize(loaded_text):
    max_tokens = 864

    # Initialize the base language model
    base_llm = Together(
        model="mistralai/Mixtral-8x22B-Instruct-v0.1",
        together_api_key=TOGETHER_API_KEY,
        max_tokens=3500,  # Set the max_tokens value here
    )

    custom_llm = CustomMaxTokenLLM(llm=base_llm, max_tokens=max_tokens)

    # Define multiple prompts
    prompts = [  # TODO: move to its own file
        """Schreiben Sie eine Zusammenfassung des folgenden Textes mit maximal 864 Token:

        {text}

        ZUSAMMENFASSUNG:""",
        """Erstellen Sie eine prägnante und umfassende Zusammenfassung des bereitgestellten Artikels mit einer maximalen Länge von 864 Tokens. Halten Sie sich an folgende Richtlinien:

    Erstellen Sie eine Zusammenfassung, die detailliert, gründlich, ausführlich und komplex ist und dabei Klarheit und Prägnanz behält.

    Integrieren Sie Hauptgedanken und wesentliche Informationen, entfernen Sie überflüssige Inhalte und konzentrieren Sie sich auf zentrale Aspekte.

    Verlassen Sie sich strikt auf den bereitgestellten Text, ohne Einbeziehung externer Informationen:

        {text}

        ZUSAMMENFASSUNG:""",
        """Schreiben Sie eine Zusammenfassung des folgenden Textes mit einer maximalen Länge von 864 Tokens. Schreiben Sie die Zusammenfassung so, dass sie ein Kleinkind verstehen würde:

        {text}

        ZUSAMMENFASSUNG:""",
    ]

    # Process each prompt and store the output in the appropriate column
    for i, prompt in enumerate(prompts):
        prompt_template = PromptTemplate(
            template=prompt, input_variables=["text"]
        )

        # Define the summarization chain for the current prompt
        chain = load_summarize_chain(
            custom_llm, chain_type="stuff", prompt=prompt_template, verbose=True
        )

        # Generate the summary for the current prompt
        summary = chain.invoke(loaded_text)
        output = summary["output_text"]
        print(f"Prompt {i+1} Summary: {output}")

    # def summarize(loaded_text):
    # # Instantiate LLM
    # # llm = Ollama(model="phi3")

    # # Define prompt
    # template = """Schreiben Sie eine Zusammenfassung des folgenden Textes:

    # {text}

    # ZUSAMENFASSUNG:"""
    # prompt_template = PromptTemplate(
    #     template=template, input_variables=["text"]
    # )
    # # loaded_text = load_data(doc)
    # summary = chain.invoke(get_text_chunks_langchain(loaded_text))
    # output = summary["output_text"]
    # print(output)
    # save_summary(output)
    # return output
