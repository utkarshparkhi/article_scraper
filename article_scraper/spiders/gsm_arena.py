import scrapy
from bs4 import BeautifulSoup


class GSMArena(scrapy.Spider):
    name = "GSM"
    base_url = "https://www.gsmarena.com/"

    def start_requests(self):
        urls = [f"https://www.gsmarena.com/res.php3?sSearch={self.product}"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.get_review_page)

    def get_review_page(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        review_links = soup.find(id="reviews").find_all("div", {"class": "review-item-media-wrap"})
        for link in review_links:
            yield scrapy.Request(url=self.base_url + link.a["href"], callback=self.get_review)

    def get_review(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        review = soup.find(id="review-body")
        url = response.url.split('/')[-1].split('.')[0]
        filename = f'GSM-review-{self.product}-{url}.txt'
        with open(filename, 'a') as f:
            f.write(review.text)
            f.write('\n')
        next_page_url = soup.find("div", {"class": "article-pages col"}).a['href']
        yield scrapy.Request(url=self.base_url+next_page_url,callback=self.get_review)
