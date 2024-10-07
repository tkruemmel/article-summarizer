import app.kgk_controller as KGKcontroller
from bs4 import BeautifulSoup


def get_posts(url="https://klassegegenklasse.org/wp-json/wp/v2/posts?per_page=100"):
    posts = []
    fetch_posts = KGKcontroller.fetch_latest_posts(url)
    for post in fetch_posts:
        post_data = {"title": BeautifulSoup(post["title"]["rendered"], features="html.parser").get_text(),
                "content": BeautifulSoup(post["content"]["rendered"], features="html.parser").get_text().replace("\n", "").replace("\xa0", "")}
        posts.append(post_data)
    return posts


#posts = get_posts()
#print(posts)
#print(len(posts))
