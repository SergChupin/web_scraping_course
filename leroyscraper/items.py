# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Compose, MapCompose, TakeFirst


def price_to_int(value):
    if value:
        value = int(value.replace(' ', ''))
    return value


def process_symbols(value):
    if value:
        value = value.replace(' ', '').replace('\n', '')
    return value


def rescale_img(value):
    if value:
        value = value.replace('w_82,h_82', 'w_1200,h_1200')
    return value


class LeroyscraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field(input_processor=MapCompose(rescale_img()))
    specifications = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(price_to_int))
    _id = scrapy.Field()
