"""
Зарегистрироваться на https://openweathermap.org/api и написать функцию,
которая получает погоду в данный момент для города,
название которого получается через input.
"""

import os
import requests
from dotenv import load_dotenv


load_dotenv("./.env")
key = "API_OW"
open_key = os.getenv(key, None)


def get_response(city, api_key):
    try:
        main_link = "http://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": api_key}
        response = requests.get(main_link, params=params)
        j_body = response.json()
        return j_body
    except Exception:
        return None


user_city = input('City: ')
