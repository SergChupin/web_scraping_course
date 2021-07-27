import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from leroyscraper.items import LeroyscraperItem


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['http://leroymerlin.ru/']

    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://spb.leroymerlin.ru/search/?q={query}"]

    def parse(self, response:HtmlResponse):
        links = response.xpath('//a[@data-qa="product-name"]')
        for link in links:
            yield response.follow(link, callback=self.parse_item)
        next_page = response.xpath('//a[contains(@data-qa-pagination-item, "right")]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_item(self,response:HtmlResponse):
        loader = ItemLoader(item=LeroyscraperItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        loader.add_xpath('images', '//img[@slot="thumbs"]/@src')
        loader.add_xpath('specifications', '//dt[@class="def-list__term"]/text()' + ' -> '
                         + '//dd[@class="def-list__definition"]/text()')
        loader.add_value('url', response.url)
        yield loader.load_item()
