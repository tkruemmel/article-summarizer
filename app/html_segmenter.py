from bs4 import BeautifulSoup


class HTMLSegmenter:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def segment(self):
        segments = []
        paragraphs = self.soup.find_all('p')

        for p in paragraphs:
            segment_type = 'paragraph'
            if p.find('a'):
                segment_type = 'paragraph_with_links'
            if p.find('b'):
                segment_type = 'bold_paragraph'

            inner_content = p.get_text()

            segments.append({'type': segment_type, 'content': inner_content})

        return segments
