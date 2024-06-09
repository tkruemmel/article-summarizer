import requests

def fetch_latest_posts(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        posts = response.json()
        return posts

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    url = "https://klassegegenklasse.org/wp-json/wp/v2/posts"
    posts = fetch_latest_posts(url)

    if posts:
        for post in posts:
            #breakpoint()
            print(f"Title: {post['title']['rendered']}")
            print(f"Date: {post['date']}")
            print(f"Link: {post['link']}")
            print(f"Content: {post['content']['rendered']}")
            print('-' * 40)
    else:
        print("Failed to retrieve posts.")
