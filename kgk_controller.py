import requests
from html_segmenter import HTMLSegmenter

def fetch_latest_posts(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        posts = response.json()
        return posts

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def search_posts(url, search_string):
    try:
        search_url = f"{url}?search={search_string}"
        response = requests.get(search_url)
        response.raise_for_status()  # Check if the request was successful

        posts = response.json()
        return posts

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while searching: {e}")
        return None

if __name__ == "__main__":
    base_url = "https://klassegegenklasse.org/wp-json/wp/v2/posts"    
    # Example search string
    search_string = "Warum wir zum ungültig wählen aufrufen"
    search_results = search_posts(base_url, search_string)
    
    if search_results:
        print("Search Results:")
        for post in search_results:
            # print(f"Title: {post['title']['rendered']}")
            # print(f"Date: {post['date']}")
            # print(f"Link: {post['link']}")
            # print(f"Content: {post['content']['rendered']}")
            # print('-' * 40)
            if not post['title']['rendered'].lower() == search_string.lower():
                continue
            segmenter = HTMLSegmenter(post['content']['rendered'])
            segments = segmenter.segment()
            for segment in segments:
                print(segment['content'])
    else:
        print("No posts found for the given search string.")

    # if search_results:
    #     print("Search Results:")
    #     for post in search_results:
    #         print(f"Title: {post['title']['rendered']}")
    #         print(f"Date: {post['date']}")
    #         print(f"Link: {post['link']}")
    #         print(f"Content: {post['content']['rendered']}")
    #         print('-' * 40)
    # else:
    #     print("No posts found for the given search string.")
