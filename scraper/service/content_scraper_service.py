from bs4 import BeautifulSoup
import requests
import urllib.request
import http.client

from scraper.model.content import Content


class ContentScraperService:
    BLACKLIST = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head',
        'input',
        'script',
        'style',
        'footer',
        'aside',
        'title',
        'alt'
    ]

    @staticmethod
    def scrape_page(url):
        try:
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            headers = {'User-Agent': user_agent}
            request = requests.get(url, headers)
            response = request.content
            return BeautifulSoup(response, 'html.parser')
        except:
            print("An error occured with " + url)
            return 'error'

    def get_page_content(self, url):
        soup = self.scrape_page(url)
        if soup == 'error':
            return None
        page_title = soup.title.string
        content = soup.find_all(text=True)

        page_text_content = ''

        for t in content:
            if t.parent.name not in self.BLACKLIST:
                page_text_content += '{} '.format(t)

        return Content(page_title, page_text_content)
