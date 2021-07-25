import scrapy
from bs4 import BeautifulSoup

from article_scraper.constant.custom_search import API_KEY, SEARCH_ID
from article_scraper.constants import *
from article_scraper.utils import writer


class CustomSearch(scrapy.Spider):
    name = "google-custom-search"

    def start_requests(self):
        url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ID}&q={self.product}"
        yield scrapy.Request(url=url, callback=self.get_links)

    def get_links(self, response):

        res = response.json()
        res = res['items']
        for r in res[:3]:
            yield scrapy.Request(url=r['link'], callback=self.find_spider(r['link'], r['displayLink']))

    def find_spider(self, url, display_link):
        if display_link == "www.theverge.com":
            return self.verge_get_review

    def verge_get_review(self, response):
        kwargs = {}
        soup = BeautifulSoup(response.body, "html.parser")
        text = soup.find("div", {"class": "c-entry-content"})
        if text is None:
            text = soup.find("div", {"class": "l-col__main"}).text
        else:
            text = text.text
        score = soup.find("span", {"class": "c-scorecard__score-number"})
        if score is not None:
            score = score.text.split()[0]
            kwargs.update({RATING: score})

        pub_date = soup.time
        if soup.time is not None:
            pub_date = pub_date['datetime']
            kwargs.update({PUB_DATE: pub_date})
        kwargs.update({DOMAIN: "verge", "queries": [self.product]})
        writer.dump_data(text, response.url, **kwargs)
