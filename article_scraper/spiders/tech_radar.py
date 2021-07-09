import scrapy
from bs4 import BeautifulSoup

from article_scraper.utils import writer


class TechRadar(scrapy.Spider):
    name = "tech_radar"

    def start_requests(self):
        url = f"https://www.techradar.com/filter/search?searchTerm={self.product}&articleType=review"
        yield scrapy.Request(url=url, callback=self.get_review_page)

    def get_review_page(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        links = soup.find_all("a")
        for link in links:
            yield scrapy.Request(url=link["href"], callback=self.get_review)

    def get_review(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        review = soup.find(id="article-body")
        paras = review.find_all("p")
        url = response.url.split('/')[-1]
        text = '\n'.join([p.text for p in paras])
        filename = f"tech_radar*review*{self.product}*{url}.txt"
        writer.write(text, filename)
