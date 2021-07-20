import time
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

DRIVER_PATH = './chromedriver.exe'
url = "https://vk.com/tokyofashion"

# Ввод для поиска в постах группы
user_input = input("Введите слово для поиска: ")

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(DRIVER_PATH, options=options)

driver.get(url)

# Сначала скрол страницы, чтобы собрать больше постов
for i in range(5):
    driver.find_element_by_xpath("//body").send_keys(Keys.END, Keys.ESCAPE)
    # END для скроллинга, ESC для убирания всплывающего окна
    time.sleep(2)

# теперь вводим наш запрос
wall_search = driver.find_element_by_xpath('//a[contains(@class, "ui_tab_search")]')
wall_search.send_keys(Keys.ENTER)
search_request = driver.find_element_by_xpath('//input[contains(@class, "ui_search_field")]')
search_request.send_keys(user_input)
search_request.send_keys(Keys.ENTER)

# сохраняем данные
post_data = []
posts = driver.find_element_by_xpath('//a[contains(@class, "post_link")]')
for i in posts:
    post_data_info = {}

    date = posts.find_element_by_class_name('rel_date')
    post_data_info['Post date'] = date.text.replace('\xa0', ' ')

    text = posts.find_element_by_class_name('wall_post_text')
    post_data_info['Post text'] = text.text

    link = posts.find_element_by_class_name('post_link')
    post_data_info['Post link'] = link.get_attribute('href')

    number_of_likes = posts.find_element_by_class_name('like_button_count')
    post_data_info['Number of likes'] = number_of_likes.text[0]

    number_of_reposts = posts.find_element_by_class_name('like_button_count')
    post_data_info['Number of reposts'] = number_of_likes.text[1]

    number_of_views = posts.find_element_by_class_name('like_views')
    post_data_info['Number of views'] = number_of_views.text

    post_data.append(post_data_info)

with MongoClient('localhost', 27017) as client:
    db = client('TokyoFashion posts')
    posts = db['posts_collection']
    posts.insert_many(post_data_info)

driver.quit()
