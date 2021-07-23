import scrapy
from scrapy.http import HtmlResponse
from jobparser.jobparser.items import JobparserItem


ITEM_SELECTORS = {
    "title": '//div[contains(@class, "f-test-search-result-item")]//a[contains(@class, "f-test-link-")]/text()',
    "salary": '//span[contains(@class, "f-test-text-company-item-salary")]//text()'
}


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://spb.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        item_urls = response.xpath('//a[contains(@class, "f-test-link-")]/@href').getall()
        for link in item_urls:
            yield response.follow(link, callback=self.parse_item)

        next_page = response.xpath('//a[contains(@class, "f-test-link-Dalshe")]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_item(self, response: HtmlResponse):
        item = JobparserItem()
        for key, xpath in ITEM_SELECTORS.items():
            item[key] = response.xpath(xpath)
        item['title'] = item['title'].get()
        item['salary'] = item['salary'].getall()
        item['url'] = response.url
        item['source'] = 'superjob.ru'
        yield item
