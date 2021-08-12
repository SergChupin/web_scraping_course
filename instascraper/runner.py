import os

from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from instascraper import settings
from instascraper.spiders.instagram import InstagramSpider

if __name__ == "__main__":
    load_dotenv(".env")
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    user_to_parse = input("Input users separated by spacebar:\n").split(' ')

    process = CrawlerProcess(settings=crawler_settings)
    kwargs = {
        "login": login,
        "password": password,
        "user_to_parse": user_to_parse,
    }
    process.crawl(InstagramSpider, **kwargs)

    process.start()
