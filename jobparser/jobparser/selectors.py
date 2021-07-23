NAVIGATION_SELECTORS = {
    "parse_item": '//div[@class="vacancy-serp"]'\
                 '/div[contains(@data-qa, "vacancy-serp__vacancy")]'\
                 '//a[contains(@data-qa, "vacancy-title"]/@href',
    "parse": '//a[contains(@data-qa, "page-next")]/@href'
}


ITEM_SELECTORS = {
    "title": '//h1/text()',
    "salary": '//p[contains(@class, "vacancy-salary")]//text()'
}
