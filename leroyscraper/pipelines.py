# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from pymongo import MongoClient


def list_to_dict(specifications):
    new_list = {}
    for i in range(len(specifications)//2):
        i *= 2
        new_list[specifications[i]] = specifications[i+1]
    return new_list


class LeroyscraperPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_db = client.leroymerlin

    def process_item(self, item, spider):
        collection = self.mongo_db[spider.name]
        item['specifications'] = list_to_dict(item['specifications'])
        if len(list(collection.find({'url': item['url']}))) < 1:
            collection.insert_one(item, upsert=True)
        return item


class LeroyImagesPipeline:
    def get_media_requests(self, item, info):
        if item["images"]:
            for img_link in item["images"]:
                try:
                    yield scrapy.Request(img_link)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['images'] = [x[1] for x in results if x[0]]
        return item
