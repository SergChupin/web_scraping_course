# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from jobparser.jobparser.settings import MONGO_HOST, MONGO_PORT
# from itemadapter import ItemAdapter


class JobparserPipeline:
    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        self.db = self.client.vacancies

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        if item['source'] == 'hh.ru':
            salary_min, salary_max, currency = self.hh_salary_filter(item['salary'])
            item['salary_min'] = salary_min
            item['salary_max'] = salary_max
            item['currency'] = currency
        elif item['source'] == 'superjob.ru':
            salary_min, salary_max, currency = self.sj_salary_filter(item['salary'])
            item['salary_min'] = salary_min
            item['salary_max'] = salary_max
            item['currency'] = currency

        del item['salary']
        collection.insert_many(item, upsert=True)

        return item

    def hh_salary_filter(self, salary):
        salary = salary[0].replace('\xa0', '').split(' ')
        if 'з/п' in salary:
            salary_min = None
            salary_max = None
            currency = None
            return salary_min, salary_max, currency

        elif 'от' in salary:
            if 'до' in salary:
                salary_min = float(salary[1])
                salary_max = float(salary[-2])
                currency = salary[-1]
                return salary_min, salary_max, currency
            else:
                salary_min = float(salary[1])
                salary_max = None
                currency = salary[-1]
                return salary_min, salary_max, currency

        elif 'до' in salary:
            salary_min = None
            salary_max = float(salary[-2])
            currency = float(salary[-1])
            return salary_min, salary_max, currency

    def sj_salary_filter(self, salary):
        if 'от' in salary:
            salary = salary[2].split('\xa0')
            currency = salary.pop()
            salary_min = float(''.join(salary))
            salary_max = None
            return salary_min, salary_max, currency

        elif 'до' in salary:
            salary = salary[2].split('\xa0')
            currency = salary.pop()
            salary_min = None
            salary_max = float(''.join(salary))
            return salary_min, salary_max, currency

        elif 'По' in salary:
            salary_min = None
            salary_max = None
            currency = None
            return salary_min, salary_max, currency

        elif '-' in salary:
            salary = [salary[0].replace('\xa0', ''), salary[4].replace('\xa0', ''), salary[6]]
            salary_min = float(salary[0])
            salary_max = float(salary[1])
            currency = salary[-1]
            return salary_min, salary_max, currency
