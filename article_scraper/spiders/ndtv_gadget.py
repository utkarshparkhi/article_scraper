import scrapy
from bs4 import BeautifulSoup

from article_scraper.utils import writer


class NDTVGadgets(scrapy.Spider):
    name = "ndtv"
    urls = []

    def start_requests(self):
        self.urls.append(
            (f"https://gadgets.ndtv.com/search?searchtext={self.product}", 'product_search')
        )
        for url in self.urls:
            yield scrapy.Request(url=url[0], callback=self.get_product)

    def get_product(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        products = soup.find(id="productSearch")
        for a in products.find_all('a'):
            yield scrapy.Request(url=a['href'], callback=self.get_review_page)

    def get_review_page(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        review = soup.find(id='review')
        if review is not None:
            review_link = review.find_all('a')[-1]['href']
            yield scrapy.Request(url=review_link, callback=self.get_review)

    def get_review(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        date = soup.find("div", {"class": "dateline"})
        kwargs = {}
        if date is not None:
            date = date.text.split("Updated:")[1].strip()
            kwargs.update({"pub_date": date})
        rating = soup.find("div", {"class": "avg_rating"})
        if rating is not None:
            rating = rating.i.get("class")
            if isinstance(rating, list):
                if len(rating) > 0:
                    kwargs.update({"rating": rating[1][-1]})
        comments = soup.find(id="btncc").text
        if len(comments)==0:
            comments = 0
        kwargs.update({"comments": comments})
        review = soup.find(id="center_content_div").find("div", {"class": "content_text row description"})
        review_text = review.text
        url = response.url
        kwargs.update({"domain":self.name})
        writer.dump_data(review_text, url, **kwargs)
