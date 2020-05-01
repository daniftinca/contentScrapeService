import re

from bs4 import BeautifulSoup
import requests
import urllib
import http.client

from scraper.service.content_scraper_service import ContentScraperService


class GoogleSearchScraperService:

    def __init__(self, content_scraper_service=ContentScraperService()):
        self.content_scraper_service = content_scraper_service

    REGEX = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    @staticmethod
    def scrape_page(url):
        try:
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            headers = {'User-Agent': user_agent}
            request = requests.get(url, headers)
            response = request.content
            return BeautifulSoup(response, 'html.parser')
        except:
            print("Couldn't get content for: " + url)
            return "error"

    @staticmethod
    def construct_url(query):
        return "https://www.google.com/search?q=" + query.replace(" ", "+")

    def get_search_result(self, query):
        soup = self.scrape_page(self.construct_url(query))
        if soup == 'error':
            return None
        links = []

        for item in soup.findAll("div", {"class": "ZINbbc xpd O9g5cc uUPGi"}):
            anchors = item.find_all('a')
            if len(anchors) > 0:
                link = anchors[0].get('href')[7:]
                if re.match(self.REGEX, link):
                    links.append(link.split('&')[0])

        return links

    def get_search_result_with_content(self, query):
        found_links = self.get_search_result(query)

        list_content = []

        for link in found_links:
            list_content.append(self.content_scraper_service.get_page_content(link))

        return list_content
