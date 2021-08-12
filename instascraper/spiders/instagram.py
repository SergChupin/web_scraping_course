import json
import re
import scrapy
from scrapy.http import HtmlResponse
from instascraper.items import InstagramScraperItem


class InstagramSpider(scrapy.Spider):
    name = "instagram"
    allowed_domains = ["instagram.com"]
    start_urls = ["https://www.instagram.com/"]
    login_url = "https://www.instagram.com/accounts/login/ajax/"
    template_user_url = "/%s"
    url_links_template = "https://i.instagram.com/api/v1/friendships/%s/%s/?count=12&search_surface=follow_list_page&%s"
    types_link_arr = ['followers', 'following']

    def __init__(self, login, password, users_to_parse, app_id, **kwargs):
        super().__init__(**kwargs)
        self.login = login
        self.enc_password = password
        self.users_to_parse = users_to_parse
        self.app_id = app_id

    def parse(self, response: HtmlResponse, **kwargs):
        token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            url=self.login_url,
            method="POST",
            formdata={
                "username": self.login,
                "enc_password": self.enc_password,
            },
            headers={
                "X-CSRFToken": token,
            },
            callback=self.user_login,
        )

    def user_login(self, response: HtmlResponse):
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            print("Json decode error")
            print(e)
            return
        except Exception as e:
            print(e)
            return

        if data["authenticated"]:
            for user_to_parse in self.users_to_parse:
                yield response.follow(
                    self.template_user_url % user_to_parse,
                    callback=self.user_page_parse,
                    cb_kwargs={"username": user_to_parse}
                )

    def user_page_parse(self, response: HtmlResponse, username: str):
        user_id = self.fetch_user_id(response.text, username)
        if user_id is not None:
            main_person = InstagramScraperItem()
            main_person['user_id'] = str(user_id)
            main_person['user'] = username
            yield main_person
            for type_link in self.types_link_arr:
                url = self.url_links_template % (user_id, type_link, '')
                yield response.follow(
                    url,
                    callback=self.parse_links,
                    headers={'x-ig-app-id': self.app_id},
                    cb_kwargs={
                        "user_id": user_id,
                        "type_link": type_link
                    }
                )

    def parse_links(self, response: HtmlResponse, user_id, type_link):
        response_json = response.json()
        if response_json['status'] == 'ok':
            for user_item in response_json['users']:
                yield self.parse_item(user_item, user_id, type_link)
            if 'next_max_id' in response_json:
                url = self.url_links_template % (user_id, type_link, 'max_id=' + response_json['next_max_id'])
                yield response.follow(
                    url,
                    callback=self.parse_links,
                    headers={'x-ig-app-id': self.app_id},
                    cb_kwargs={
                        "user_id": user_id,
                        "type_link": type_link
                    }
                )

    def parse_item(self, user_item, user_id, type_link):
        person = InstagramScraperItem()
        person['user_id'] = str(user_item['user_id'])
        person['user'] = user_item['username']
        person['user_photo'] = user_item['user_photo']
        if type_link == 'followers':
            person['id_following'] = str(user_id)
        else:
            person['id_follower'] = str(user_id)
        return person

    def fetch_csrf_token(self, text):
        matched = re.search('"csrf_token":"\\w+"', text).group()
        return matched.split(":").pop().replace(r'"', "")

    # get user_id for interesting user
    def fetch_user_id(self, text, username):
        matched = re.search('{"id":"\\d+","username":"%s"}' % username, text).group()
        return json.loads(matched).get("id")
