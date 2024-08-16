import requests
from html_segmenter import HTMLSegmenter
from summarizer import get_text_chunks_langchain, summarize
import sys

BASE_API_URL = "https://klassegegenklasse.org/wp-json/wp/v2/posts"
BASE_WEB_URL = "klassegegenklasse.org/"


def fetch_latest_posts(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        posts = response.json()
        return posts

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def search_posts(url, search_string):
    try:
        search_url = f"{url}?slug={search_string}"
        response = requests.get(search_url)
        response.raise_for_status()

        posts = response.json()
        if not posts:
            search_url = f"{url}?search={search_string.replace('-', ' ')}"
            response = requests.get(search_url)
            response.raise_for_status()  # Check if the request was successful
            posts = response.json()

        return posts

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while searching: {e}")
        return None

def create_full_text(text):
    segmenter = HTMLSegmenter(text)
    segments = segmenter.segment()
    full_text = ""
    for segment in segments:
        full_text += segment["content"]
    return full_text


if __name__ == "__main__":
    search_string = input("Hi there! This is an article summariser for klassegegenklasse.org. I can summarise articles that have a length of approximately 30mins or shorter, which is indicated on the website. Please enter a search term to find an article that I may summarise for you. Hit enter to confirm: ")
    base_url = "https://klassegegenklasse.org/wp-json/wp/v2/posts"
    search_results = search_posts(base_url, search_string)
    
    if search_results:
        print("Search Results:")
        for i, post in enumerate(search_results):
            print(f"{i+1}. {post['title']['rendered']}")

        choice = int(input("These are the search results. Enter the number of the article you want to choose: ")) - 1

        if 0 <= choice < len(search_results):
            chosen_post = search_results[choice]
            full_text = create_full_text(chosen_post['content']['rendered'])
            langchain_doc = get_text_chunks_langchain(full_text)
            summarize(langchain_doc, chosen_post['title']['rendered'], "results.csv")
            
    else:
        print("No posts found for the given search string.")
