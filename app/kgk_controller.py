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
    # TODO: is this check needed? are there variations on the base web url?
    if BASE_WEB_URL not in search_url:
        return None

    # remove trailing slash if necessary
    search_url = search_url[:-1] if search_url[-1] == '/' else search_url
    slug = search_url.split("/")[-1]

    # search by slug first, then try by search terms from slug
    for search_string, search_func in [
        (slug, search_posts_by_slug),
        (slug.replace('-', ' '), search_posts_by_search_strings),
        # TODO: can remove, searching by tags wasn't very effective
        # (slug.split('-'), search_posts_by_tags),
    ]:
        content = search_func(BASE_API_URL, search_string)
        # check found posts for one with matching slug
        if len(content) > 0:
            for post in content:
                if slug == post.get('slug', ''):
                    return post
    return None


if __name__ == "__main__":
    # Example search string
    search_string = "Warum wir zum ungültig wählen aufrufen"
    search_results = search_posts_by_search_strings(BASE_API_URL, search_string)

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
