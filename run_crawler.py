from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from article_scraper.spiders import ndtv_gadget, gsm_arena, CustomSearch

def scrape(product):
    process = CrawlerProcess(get_project_settings())
    process.crawl(gsm_arena.GSMArena, product=product)
    process.crawl(ndtv_gadget.NDTVGadgets, product=product)
    process.crawl(CustomSearch.CustomSearch, product=product)
    process.start()

scrape("oppo reno 6")
