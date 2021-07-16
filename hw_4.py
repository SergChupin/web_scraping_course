import requests
from pymongo import MongoClient
from lxml.html import fromstring


def upsert_news(info):
    get_source = info.get('source')
    get_title = info.get('title')
    get_link = info.get('link')
    get_datetime = info.get('datetime')

    key = {'title': get_title}
    data = {
        '$set': {
            'link': get_link, 'datetime': get_datetime, 'source': get_source
        }
    }

    with MongoClient('localhost', 27017) as client:
        db = client['news_collection']
        news = db.news
        news.update_one(key, data, upsert=True)


def get_news_mail():

    url = "https://news.mail.ru/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    dom = fromstring(response.text)

    base_items_xpath = '//ul[contains(@class, "list list_type_square list_half js-module")]/li'
    new_items_xpath = '//div[contains(@class, "article js-article")]'

    title_xpath = './a//text()'
    link_xpath = './a/@href'
    datetime_xpath = './/span[contains(@class, "note__text")]//@datetime'
    source = './/span[contains(@class, "link__text")]/text()'

    news = dom.xpath(base_items_xpath)

    for n in news:
        info = {}
        info['title'] = n.xpath(title_xpath)[0].replace('\xa0', ' ')
        info['link'] = n.xpath(link_xpath)[0]
        n_url = n.xpath(link_xpath)[0]
        n_response = requests.get(n_url, headers=headers)
        n_dom = fromstring(n_response.text)
        news_info = n_dom.xpath(new_items_xpath)
        info['datetime'] = news_info[0].xpath(datetime_xpath)[0]
        info['source'] = news_info[0].xpath(source)[0]

        upsert_news(info)


def get_news_lenta():

    url = "https://lenta.ru/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    dom = fromstring(response.text)

    items_xpath = '//div[contains(@class, "main__content")]//div[contains(@class, "item")]' \
                  '//time[contains(@class, "g-time")]/..'

    title_xpath = './text()'
    link_xpath = './@href'
    datetime_xpath = './/@datetime'
    source = 'lenta.ru'

    news = dom.xpath(items_xpath)

    for n in news:
        info = {}
        info['title'] = n.xpath(title_xpath)[0].replace('\xa0', ' ')
        info['link'] = url + n.xpath(link_xpath)[0]
        info['datetime'] = n.xpath(datetime_xpath)
        info['source'] = source

        upsert_news(info)


def get_news_yandex():

    url = "https://yandex.ru/news"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    dom = fromstring(response.text)

    items_xpath = '//div[contains(@class, "mg-grid__col")]/article[contains(@class, "mg-card")]'

    title_xpath = './/h2/text()'
    link_xpath = './/a//@href'
    datetime_xpath = './/span[contains(@class, "mg-card-source__time")]/text()'
    source = './/span[contains(@class, "mg-card-source__source")]//a/text()'

    news = dom.xpath(items_xpath)

    for n in news:
        info = {}
        info['title'] = n.xpath(title_xpath)[0].replace('\xa0', ' ')
        info['link'] = n.xpath(link_xpath)[0]
        info['datetime'] = n.xpath(datetime_xpath)
        info['source'] = n.xpath(source)[0]

        upsert_news(info)


scrapping_news = [get_news_mail(), get_news_lenta(), get_news_yandex()]
