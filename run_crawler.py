from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from article_scraper.spiders import ndtv_gadget, gsm_arena, CustomSearch


def get_process():
    return CrawlerProcess(get_project_settings())


def scrape(process, product, queries):
    process.crawl(gsm_arena.GSMArena, product=product, queries=queries)
    # process.crawl(ndtv_gadget.NDTVGadgets, product=product, queries=queries)
    # process.crawl(CustomSearch.CustomSearch, product=product, queries=queries)


def add_queries(products, qdict):
    process = get_process()
    for product in products:
        scrape(process, product, list(qdict[product]))
    process.start()
