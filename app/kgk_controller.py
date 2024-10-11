import requests

from html_segmenter import HTMLSegmenter
from summarizer import get_text_chunks_langchain, summarize
import sys

BASE_API_URL = "https://klassegegenklasse.org/wp-json/wp/v2/posts"
BASE_WEB_URL = "klassegegenklasse.org/"


def create_full_text(text):
    segmenter = HTMLSegmenter(text)
    segments = segmenter.segment()
    full_text = ""
    for segment in segments:
        full_text += segment["content"]
    return full_text


def fetch_latest_posts(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        posts = response.json()
        return posts

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def search_posts_by_search_strings(url, search_strings):
    try:
        search_url = f"{url}?search={search_strings}"
        response = requests.get(search_url)
        response.raise_for_status()
        posts = response.json()
        return posts

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while searching: {e}")
        return None


# was not particularly helpful
def search_posts_by_tags(url, search_tags):
    try:
        search_url = f"{url}?search={search_tags}"
        response = requests.get(search_url)
        response.raise_for_status()
        posts = response.json()
        return posts

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while searching: {e}")
        return None


def search_posts_by_slug(url, search_string):
    try:
        search_url = f"{url}?slug={search_string}"
        response = requests.get(search_url)
        response.raise_for_status()

        posts = response.json()
        return posts

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while searching: {e}")
        return None


def find_specific_post(search_url):
    if BASE_WEB_URL not in search_url:
        return None

    # remove trailing slash if necessary
    search_url = search_url[:-1] if search_url[-1] == '/' else search_url
    slug = search_url.split("/")[-1]

    # search by slug first, then try by search terms from slug
    for search_string, search_func in [
        (slug, search_posts_by_slug),
        (slug.replace('-', ' '), search_posts_by_search_strings),
    ]:
        content = search_func(BASE_API_URL, search_string)
        # check found posts for one with matching slug
        if len(content) > 0:
            for post in content:
                if slug == post.get('slug', ''):
                    return post
    return None


def find_all_relavent_posts(search_url):
    if BASE_WEB_URL not in search_url:
        return None

    # remove trailing slash if necessary
    search_url = search_url[:-1] if search_url[-1] == '/' else search_url
    slug = search_url.split("/")[-1]

    # search by slug first, then try by search terms from slug
    for search_string, search_func in [
        (slug, search_posts_by_slug),
        (slug.replace('-', ' '), search_posts_by_search_strings),
    ]:
        content = search_func(BASE_API_URL, search_string)
        # check found posts for one with matching slug
        if len(content) > 0:
            return content
    return None


if __name__ == "__main__":
    search_string = input(
        "Hi there! This is an article summariser for klassegegenklasse.org. I can summarise articles that have a length of approximately 30mins or shorter, which is indicated on the website. Please enter a search term to find an article that I may summarise for you. Hit enter to confirm: "
    )
    # search_results = search_posts(base_url, search_string)
    print('first:, ', search_string)
    search_results = find_all_relavent_posts(search_string)

    if search_results:
        print("Search Results:")
        for i, post in enumerate(search_results):
            print(f"{i+1}. {post['title']['rendered']}")

        choice = (
            int(
                input(
                    "These are the search results. Enter the number of the article you want to choose: "
                )
            )
            - 1
        )

        if 0 <= choice < len(search_results):
            chosen_post = search_results[choice]
            full_text = create_full_text(chosen_post['content']['rendered'])
            langchain_doc = get_text_chunks_langchain(full_text)
            _ = summarize(langchain_doc)

    else:
        print("No posts found for the given search string.")
