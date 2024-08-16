import json
from bs4 import BeautifulSoup
import csv
#from kgk_controller import fetch_latest_posts, search_posts
#from html_segmenter import HTMLSegmenter
from langchain_community.document_loaders import JSONLoader, TextLoader
from langchain_community.llms import Ollama
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema.document import Document
# Querying code and language models with Together AI

from langchain_together import Together

from custom_max_token_llm import CustomMaxTokenLLM

import os

os.environ["ANYSCALE_API_BASE"] = "https://api.endpoints.anyscale.com/v1"
os.environ["ANYSCALE_API_KEY"] = "DUMMY"




# # Isolating one post to experiment with
# def get_test_post(url="https://klassegegenklasse.org/wp-json/wp/v2/posts"):
#     posts = fetch_latest_posts(url)
#     post = posts[3]["content"]["rendered"]
#     stripped_post = BeautifulSoup(post, features="html.parser").get_text()
#     with open("post.txt","w+") as file:
#         file.writelines(stripped_post)
#     return None


# def get_csv(): # ??? need to figure out how to load KGK data into LangChain Documents


# def get_json(): # json to lc Document?
#     posts = fetch_latest_posts("https://klassegegenklasse.org/wp-json/wp/v2/posts")
#     with open("posts.json", "w") as outfile:
#         json.dump(posts, outfile)
#     return None


def load_data(doc):
    loader = TextLoader(doc)
    data = loader.load()
    return data


# def load_data():
# loader = JSONLoader(file_path="posts.json", jq_schema=".", content_key="content")
# data = loader.load()
# return None


def save_summary(summary):
    with open("summary.txt", "w+") as file:
        file.writelines(summary)

def get_text_chunks_langchain(text):
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = [Document(page_content=x) for x in text_splitter.split_text(text)]
    return docs

def summarize(loaded_text, article_name, csv_file_path):
    max_tokens = 864

    # Initialize the base language model
    base_llm = Together(
        model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        together_api_key=TOGETHER_API_KEY,
        max_tokens=max_tokens  # Set the max_tokens value here
    )

    # Define multiple prompts
    prompts = [
        """Schreiben Sie eine Zusammenfassung des folgenden Textes:

        {text}

        ZUSAMMENFASSUNG:""",
        
        """Erstellen Sie als professioneller Zusammenfassender eine prägnante und umfassende Zusammenfassung des bereitgestellten Artikels mit einer maximalen Länge von 864 Tokens. Halten Sie sich an folgende Richtlinien:

    Erstellen Sie eine Zusammenfassung, die detailliert, gründlich, ausführlich und komplex ist und dabei Klarheit und Prägnanz behält.

    Integrieren Sie Hauptgedanken und wesentliche Informationen, entfernen Sie überflüssige Inhalte und konzentrieren Sie sich auf zentrale Aspekte.

    Verlassen Sie sich strikt auf den bereitgestellten Text, ohne Einbeziehung externer Informationen:

        {text}

        ZUSAMMENFASSUNG:""",
        
        """Schreiben Sie eine Zusammenfassung des folgenden Textes mit einer maximalen Länge von 864 Tokens. Schreiben Sie die Zusammenfassung so, dass sie ein Kleinkind verstehen würde:

        {text}

        ZUSAMMENFASSUNG:"""
    ]

    # Define custom column headers
    fieldnames = ["Article", "short_prompt", "extended_prompt", "short_prompt_max_len"]

    # Read or create the CSV file
    rows = []
    if os.path.exists(csv_file_path):
        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Ensure the 'Article' column exists in the row
                if "Article" not in row:
                    row["Article"] = ""
                rows.append(row)
            # Ensure the CSV file has the correct headers
            if reader.fieldnames != fieldnames:
                raise ValueError(f"CSV file headers do not match the expected headers: {fieldnames}")
    else:
        rows = []

    # Check if the article already exists in the CSV
    row_exists = False
    for row in rows:
        if row["Article"] == article_name:
            row_exists = True
            break

    # Create a new row or overwrite the existing one
    if not row_exists:
        row = {"Article": article_name}

    # Process each prompt and store the output in the appropriate column
    for i, prompt in enumerate(prompts):
        prompt_template = PromptTemplate(template=prompt, input_variables=["text"])
        
        # Define the summarization chain for the current prompt
        chain = load_summarize_chain(
            base_llm, chain_type="stuff", prompt=prompt_template, verbose=True
        )
        
        # Generate the summary for the current prompt
        summary = chain.invoke(loaded_text)
        output = summary["output_text"]
        print(f"Prompt {i+1} Summary: {output}")
        
        # Save the output to the corresponding column in the row
        if i == 0:
            row["short_prompt"] = output
        elif i == 1:
            row["extended_prompt"] = output
        elif i == 2:
            row["short_prompt_max_len"] = output

    # Write the updated row back to the CSV
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Write the header if the CSV is empty or newly created
        if not rows:
            writer.writeheader()
        
        # Write all rows, including the updated one
        if row_exists:
            for r in rows:
                if r["Article"] == article_name:
                    r.update(row)
                writer.writerow(r)
        else:
            rows.append(row)
            writer.writerows(rows)

    return row


#get_test_post()
#loaded_data = load_data("post.txt")
#print(loaded_data)
#summarize("post.txt")

