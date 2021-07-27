from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leroyscraper.spiders.leroymerlin import LeroymerlinSpider
from leroyscraper import settings

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    query = "светильники"

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroymerlinSpider, query=query)

    process.start()
