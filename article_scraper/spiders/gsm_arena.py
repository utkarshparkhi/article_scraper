import re

import scrapy
from bs4 import BeautifulSoup

from article_scraper.utils import writer
from article_scraper.constants import *


class GSMArena(scrapy.Spider):
    name = "GSM"
    base_url = "https://www.gsmarena.com/"
    flen = 0

    def start_requests(self):
        urls = [f"https://www.gsmarena.com/res.php3?sSearch={self.product}"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.get_review_page,
    meta={'proxy': 'http://scraperapi:82814b162327ecde5d84e2a712ff85bb@proxy-server.scraperapi.com:8001'})

    def get_review_page(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        review_links = soup.find(id="reviews")
        if review_links is not None:
            review_links = review_links.find_all("div", {"class": "review-item-content"})

            for link in review_links:
                pub_date = link.find("span", {"class": "meta-item-time"}).text
                yield scrapy.Request(url=self.base_url + link.a["href"], callback=self.get_review,
                                     cb_kwargs={PUB_DATE: pub_date},
    meta={'proxy': 'http://scraperapi:82814b162327ecde5d84e2a712ff85bb@proxy-server.scraperapi.com:8001'}
                                     )

        product_links = soup.find(id="review-body")
        if product_links is not None:
            product_links = product_links.find_all("div", {"class": "makers"})
            if len(product_links):
                product_links = product_links[0].find_all("a")
                for link in product_links:
                    yield scrapy.Request(url=self.base_url + link['href'], callback=self.get_review_from_product,
    meta={'proxy': 'http://scraperapi:your_key@proxy-server.scraperapi.com:8001'})

    def get_review_from_product(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        review_link = soup.find_all("li", {"class": "article-info-meta-link article-info-meta-link-review light large "
                                                    "help help-review"})
        if len(review_link):
            review_link = review_link[0]
            link = review_link.a['href']
            yield scrapy.Request(url=self.base_url + link, callback=self.get_review,
    meta={'proxy': 'http://scraperapi:82814b162327ecde5d84e2a712ff85bb@proxy-server.scraperapi.com:8001'})

    def get_review(self, response, **kwargs):
        soup = BeautifulSoup(response.body, 'html.parser')
        review = soup.find(id="review-body")
        rating = soup.find("span", {"class": "score"})
        if rating is not None:
            kwargs.update({RATING: rating.text})
        url = response.url
        kwargs.update({DOMAIN: self.name})
        comments = soup.find("li", {"class": "article-info-meta-link meta-link-opinions"})
        if comments is not None:
            comments = re.search(r"\(([0-9_]+)\)", comments.text)
            comments = comments.group(1)
            kwargs.update({COMMENT_COUNT: comments})
        kwargs.update({"queries": [self.product], "domain": self.name})

        writer.dump_data(review.text, url, **kwargs)
        next_page_url = soup.find("div", {"class": "article-pages col"})
        if next_page_url is not None:
            next_page_url = next_page_url.a['href']
            yield scrapy.Request(url=self.base_url + next_page_url, callback=self.get_review, cb_kwargs=kwargs,
    meta={'proxy': 'http://scraperapi:82814b162327ecde5d84e2a712ff85bb@proxy-server.scraperapi.com:8001'})
