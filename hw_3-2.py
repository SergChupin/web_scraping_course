from pymongo import MongoClient
from pprint import pprint


client = MongoClient('localhost', 27017)
db = client['hh_jobs_db']
jobs = db.jobs

start = int(input("Вывести вакансии с зарплатой от "))
result = jobs.find({'Максимальная зарплата': {'$gt': start}},
                   {'Название вакансии': True,
                    'Ссылка на объявление': True,
                    'Максимальная зарплата': True,
                    '_id': False})

for vac in result:
    pprint(vac)

client.close()
