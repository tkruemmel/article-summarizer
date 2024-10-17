import os

from bs4 import BeautifulSoup

import app.kgk_controller as KGKcontroller


BASE_API_URL = os.environ.get('BASE_API_URL')


def get_posts(url=f'{BASE_API_URL}?per_page=100'):
    posts = []
    fetch_posts = KGKcontroller.fetch_latest_posts(url)
    for post in fetch_posts:
        post_data = {
            'title': BeautifulSoup(
                post['title']['rendered'], features='html.parser'
            ).get_text(),
            'content': BeautifulSoup(
                post['content']['rendered'], features='html.parser'
            )
            .get_text()
            .replace('\n', '')
            .replace('\xa0', ''),
        }
        posts.append(post_data)
    return posts


if __name__ == '__main__':
    posts = get_posts()
    # print(posts)
    print(len(posts))
