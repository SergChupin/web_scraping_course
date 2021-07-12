import time
import requests
from bs4 import BeautifulSoup as bs
import json


class HH_scraper:
    def __init__(self, start_url, headers, params):
        self.start_url = start_url
        self.start_headers = headers
        self.start_params = params
        self.info_vacancy = []


    def get_html_string(self, url, headers='', params=''):
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.ok:
                return response.text
        except Exception as e:
            time.sleep(1)
            print(e)
            return None

    @staticmethod
    def get_dom(html_string):
        return bs(html_string, "html.parser")

    def run(self):
        next_page = ''
        while next_page is not None:
            if next_page == '':
                html_string = self.get_html_string(self.start_url + '/search/vacancy', self.start_headers,
                                                   self.start_params)
            else:
                html_string = self.get_html_string(next_page)

            soup = HH_scraper.get_dom(html_string)
            vacancy_list = soup.findAll('div', attrs={'class': 'vacancy-serp-item'})
            self.get_info_from_element(vacancy_list)
            try:
                next_page = self.start_url + soup.find('a', attrs={'data-qa': 'pager-next'}).attrs["href"]
            except Exception as e:
                next_page = None

    def get_info_from_element(self, vacancy_list):
        for vacancy in vacancy_list:
            vacancy_data = {}
            vacancy_name = vacancy.find('a', {'class': 'bloko-link'}).getText()
            vacancy_link = vacancy.find('a', {'class': 'bloko-link'}).attrs["href"]
            vacancy_data['Название вакансии'] = vacancy_name
            vacancy_data['Ссылка на объявление'] = vacancy_link
            vacancy_data['Сайт'] = self.start_url
            self.get_salary(vacancy_data, vacancy)
            self.info_vacancy.append(vacancy_data)

    def get_salary(self, vacancy_data, vacancy):
        try:
            vacancy_salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText()
            vacancy_salary = vacancy_salary.replace('\u202f', '').split()
            if '–' in vacancy_salary:
                vacancy_data['Минимальная зарплата'] = float(vacancy_salary[2])
                vacancy_data['Максимальная зарплата'] = float(vacancy_salary[2])
                vacancy_data['Валюта'] = vacancy_salary[-1]
            elif 'от' in vacancy_salary:
                vacancy_data['Минимальная зарплата'] = float(vacancy_salary[1])
                vacancy_data['Валюта'] = vacancy_salary[-1]
            elif 'до' in vacancy_salary:
                vacancy_data['Максимальная зарплата'] = float(vacancy_salary[1])
                vacancy_data['Валюта'] = vacancy_salary[-1]

        except Exception as e:
            vacancy_data['Зарплата'] = None

    def save_info_vacancy(self):
        with open("hh.ru_vacancies.json", 'w', encoding="utf-8") as file:
            json.dump(self.info_vacancy, file, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    user_find = input('Какие вакансии надо найти?\n-- ')
    main_link_hh = "https://spb.hh.ru"
    params_main_hh = {"area": "1",
                   "fromSearchLine": "true",
                   "st": "searchVacancy",
                   "text": user_find,
                   "page": "0"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}

    scraper_hh = HH_scraper(main_link_hh, headers, params_main_hh)
    scraper_hh.run()
    scraper_hh.save_info_vacancy()
    print('\nНайденные вакансии сохранены в файл hh.ru_vacancies.json')
