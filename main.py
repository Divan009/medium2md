from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md


class MediumToMarkDownConverter:
    def __init__(self):
        self.medium_base_link = "https://medium.com/"

    def convert_from_medium_url(self, url):
        response = requests.get(url)
        response.raise_for_status()

        html = response.content

        soup = BeautifulSoup(html, 'html.parser')
        article_html = soup.find('article')

        # Convert HTML to Markdown
        title, markdown = self.custom_markdownify(str(article_html))

        return title, markdown

    def custom_markdownify(self, html):
        # Convert HTML to Markdown
        processed_lines = []
        markdown = md(html, heading_style="ATX")
        lines = markdown.split('\n')

        title = lines[0].strip().replace('#', '')
        title = title.replace('\\', '')


        for line in lines:
            if line.startswith('[') and line.endswith(']') or line.endswith(')'):
                if 'miro.medium.com' in line or 'medium.com/m/signin' in line:
                    continue
            elif 'Published in' in line:
                continue
            elif line.strip() in {'Listen', 'Share'}:
                continue

            processed_lines.append(line)

        return title, '\n'.join(processed_lines)


if __name__ == "__main__":
    converter = MediumToMarkDownConverter()
    title, markdown_text = converter.convert_from_medium_url('https://codeburst.io/web-development-back-end-with-flask-part-2-routing-a8ecfd828933')
    print(title, len(markdown_text))
    with open(f'md_file/{title}.md', 'w') as f:
        f.write(markdown_text)
