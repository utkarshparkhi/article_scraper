from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from article_scraper.spiders import ndtv_gadget, gsm_arena

process = CrawlerProcess(get_project_settings())
process.crawl(gsm_arena.GSMArena, product="galaxy s10")
process.crawl(ndtv_gadget.NDTVGadgets, product="iphone 12")
process.start()