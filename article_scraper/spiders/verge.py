import datetime

import scrapy
from bs4 import BeautifulSoup

from article_scraper.utils import writer
from article_scraper.constants import *


class Verge(scrapy.Spider):
    name = 'verge'

    def start_requests(self):
        url = f"https://www.theverge.com/search?q={self.product}"
        yield scrapy.Request(url=url, callback=self.get_review_pages)

    def get_review(self, response):
        soup = BeautifulSoup(response.body)
        text = soup.find("div", {"class": "c-entry-content "}).text
        pub_date = soup.time
        if soup.time is not None:
            pub_date = pub_date['datetime']

        kwargs = {PUB_DATE: pub_date, DOMAIN: self.name}
        writer.dump_data(text, response.url, **kwargs)
