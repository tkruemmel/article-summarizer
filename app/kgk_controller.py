import requests
from html_segmenter import HTMLSegmenter
from summarizer import get_text_chunks_langchain, summarize

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
    # remove trailing slash if necessary
    if search_string[-1] == '/':
        search_string = search_string[:-1]
    # isolate slug for content retrieval
    if BASE_WEB_URL in search_string:
        search_string = search_string.split(BASE_WEB_URL)[-1]

    try:
        search_url = f"{url}?slug={search_string}"
        response = requests.get(search_url)
        response.raise_for_status()

        posts = response.json()
        if not posts:
            search_url = f"{url}?search={search_string.replace('-', ' ')}"
            response = requests.get(search_url)
            response.raise_for_status()
            posts = response.json()

        return posts

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while searching: {e}")
        return None


if __name__ == "__main__":
    # Example search string
    search_string = "Warum wir zum ungültig wählen aufrufen"
    search_results = search_posts(BASE_API_URL, search_string)

    if search_results:
        print("Search Results:")
        for post in search_results:
            if not post['title']['rendered'].lower() == search_string.lower():
                continue
            segmenter = HTMLSegmenter(post['content']['rendered'])
            segments = segmenter.segment()
            full_text = ""
            for segment in segments:
                full_text += segment["content"]
            langchain_doc = get_text_chunks_langchain(full_text)
            summarize(langchain_doc)

    else:
        print("No posts found for the given search string.")
