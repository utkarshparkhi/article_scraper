import scrapy
from bs4 import BeautifulSoup

from article_scraper.utils import writer


class GSMArena(scrapy.Spider):
    name = "GSM"
    base_url = "https://www.gsmarena.com/"
    flen = 0

    def start_requests(self):
        urls = [f"https://www.gsmarena.com/res.php3?sSearch={self.product}"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.get_review_page)

    def get_review_page(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        review_links = soup.find(id="reviews").find_all("div", {"class": "review-item-media-wrap"})
        for link in review_links:
            yield scrapy.Request(url=self.base_url + link.a["href"], callback=self.get_review, cb_kwargs={"flen": 0})
        product_links = soup.find(id="review-body").find_all("div", {"class": "makers"})
        if len(product_links):
            product_links = product_links[0].find_all("a")
            for link in product_links:
                yield scrapy.Request(url=self.base_url + link['href'], callback=self.get_review_from_product)

    def get_review_from_product(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        review_link = soup.find_all("li", {"class": "article-info-meta-link article-info-meta-link-review light large "
                                                    "help help-review"})
        if len(review_link):
            review_link = review_link[0]
            link = review_link.a['href']
            print(link)
            yield scrapy.Request(url=self.base_url + link, callback=self.get_review, cb_kwargs={"flen": 0})

    def get_review(self, response, **kwargs):
        soup = BeautifulSoup(response.body, 'html.parser')
        review = soup.find(id="review-body")
        url = response.url.split('/')[-1].split('.')[0]
        flen = min(kwargs['flen'], len(url)) if kwargs['flen'] else len(url)
        filename = f'GSM-review-{self.product}-{url[:flen]}.txt'
        writer.write_review(review.text, filename)
        next_page_url = soup.find("div", {"class": "article-pages col"})
        if next_page_url is not None:
            next_page_url = next_page_url.a['href']
            yield scrapy.Request(url=self.base_url + next_page_url, callback=self.get_review, cb_kwargs={"flen": flen})
