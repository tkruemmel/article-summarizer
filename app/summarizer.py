import json
from bs4 import BeautifulSoup
import csv
from kgk_controller import fetch_latest_posts, search_posts
from html_segmenter import HTMLSegmenter
from langchain_community.document_loaders import JSONLoader, TextLoader
from langchain_community.llms import Ollama
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate


# Isolating one post to experiment with
def get_test_post(url="https://klassegegenklasse.org/wp-json/wp/v2/posts"):
    posts = fetch_latest_posts(url)
    post = posts[3]["content"]["rendered"]
    stripped_post = BeautifulSoup(post, features="html.parser").get_text()
    with open("post.txt", "w+") as file:
        file.writelines(stripped_post)
    return None


# def get_csv(): # ??? need to figure out how to load KGK data into LangChain Documents


def get_json():  # json to lc Document?
    posts = fetch_latest_posts(
        "https://klassegegenklasse.org/wp-json/wp/v2/posts"
    )
    with open("posts.json", "w") as outfile:
        json.dump(posts, outfile)
    return None


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


def summarize(doc):
    # Instantiate LLM
    llm = Ollama(model="phi3")

    # Define prompt
    template = """Schreiben Sie eine Zusammenfassung des folgenden Textes:

    {text}

    ZUSSAMENFASSUNG:"""
    prompt_template = PromptTemplate(
        template=template, input_variables=["text"]
    )

    # Define chain
    chain = load_summarize_chain(
        llm, chain_type="stuff", prompt=prompt_template, verbose=True
    )  # to see detailed prompt

    loaded_text = load_data(doc)
    summary = chain.invoke(loaded_text)
    output = summary["output_text"]
    print(output)
    save_summary(output)
    return output


# get_test_post()
# loaded_data = load_data("post.txt")
# print(loaded_data)
summarize("post.txt")
