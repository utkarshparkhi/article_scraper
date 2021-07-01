import scrapy
from bs4 import BeautifulSoup


class NDTVGadgets(scrapy.Spider):
    name = "ndtv"
    urls = []

    def start_requests(self):
        self.urls.append(
            (f"https://gadgets.ndtv.com/search?searchtext={'+'.join(self.product.split())}", 'product_search')
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
        review_link = review.find_all('a')[-1]['href']
        yield scrapy.Request(url=review_link, callback=self.get_review)

    def get_review(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        review = soup.find(id="center_content_div").find("div", {"class": "content_text row description"})
        review_text = review.find_all('p')
        url = response.url.split('/')[-1]
        filename = f'NDTVreview-{self.product}-{url}.txt'
        with open(filename, 'w+') as f:
            for text in review_text:
                f.write(text.text)
                f.write('\n')
