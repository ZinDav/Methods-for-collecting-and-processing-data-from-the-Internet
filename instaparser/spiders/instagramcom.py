import scrapy
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem
import re
from urllib.parse import urlencode
import json
from copy import deepcopy

# 1) Написать приложение, которое будет проходиться по указанному списку двух и/или более
# пользователей и собирать данные об их подписчиках и подписках.
# 2) По каждому пользователю, который является подписчиком или на которого подписан
# исследуемый объект нужно извлечь имя, id, фото (остальные данные по
# желанию). Фото можно дополнительно скачать.
# 4) Собранные данные необходимо сложить в базу данных. Структуру данных нужно заранее продумать, чтобы:
# 5) Написать запрос к базе, который вернет список подписчиков только указанного пользователя
# 6) Написать запрос к базе, который вернет список профилей, на кого подписан указанный пользователь


class InstagramcomSpider(scrapy.Spider):
    name = 'instagramcom'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'Onliskill_udm'
    inst_password = '#PWD_INSTAGRAM_BROWSER:10:1645067027:AfpQAFtTqEcDha3ZDFcQQtU+vaikGmOX839U1So5njVAcYMaQM2\
    +AN+T5J76jy7t/xudQfLXwf6EnTztOKYL8TVK1Gi+NGks7jfn5LVfO9alQlSN1gh363NTbcCqcaGCZ/mQghu0UZJ2MMqX119WSOOI'
    users_parse = ['techskills_2022', 'vdnh_russia']
    api_url = 'https://i.instagram.com/api/v1/friendships/257016648/'
    posts_hash = '8c2a529969ee035a5063f2fc8602a0fd'
    us = 0

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.inst_login_link,
                                 method='POST',
                                 callback=self.login,
                                 formdata={'username': self.inst_login,
                                           'enc_password': self.inst_password},
                                 headers={'X-CSRFToken': csrf})

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data['authenticated']:
            if self.us == 0:
                for user in self.users_parse:
                    yield response.follow(f'/{user}/',
                                          callback=self.user_followings_start_parse,
                                          cb_kwargs={'main_user': deepcopy(user)})
            self.us += 1
            if self.us == 1:
                for user in self.users_parse:
                    yield response.follow(f'/{user}/',
                                          callback=self.user_followers_start_parse,
                                          cb_kwargs={'main_user': deepcopy(user)})

    def user_followings_start_parse(self, response: HtmlResponse, main_user):
        main_user_id = self.fetch_user_id(response.text, main_user)
        variables = {'count': 12,
                     'search_surface': 'follow_list_page'}
        url_fer = f'{self.api_url}following/?count={variables["count"]}&search_surface={variables["search_surface"]}'
        yield response.follow(url_fer,
                              callback=self.user_followings_parse,
                              cb_kwargs={'main_user': main_user,
                                         'main_user_id': main_user_id,
                                         'variables': deepcopy(variables)},
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'})

    def user_followings_parse(self, response: HtmlResponse, main_user, main_user_id, variables):
        j_data = response.json()
        if not j_data['should_limit_list_of_followers']:
            variables["max_id"] = j_data['next_max_id']
            url_fer = f'{self.api_url}following/?count={variables["count"]}&max_id={variables["max_id"]}&search_surface={variables["search_surface"]}'
            yield response.follow(url_fer,
                                  callback=self.user_followings_parse,
                                  cb_kwargs={'main_user': main_user,
                                             'main_user_id': main_user_id,
                                             'variables': deepcopy(variables)},
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'})

        followings = j_data['users']
        for following in followings:
            item = InstaparserItem(
                type='followings',
                main_user=main_user,
                main_user_id=main_user_id,
                user_id=following['pk'],
                username=following['username'],
                full_name=following['full_name'],
                photo=following['profile_pic_url'],
                is_private=following['is_private']
            )
            yield item

    def user_followers_start_parse(self, response: HtmlResponse, main_user):
        main_user_id = self.fetch_user_id(response.text, main_user)
        variables = {'count': 12,
                     'search_surface': 'follow_list_page'}
        url_fer = f'{self.api_url}followers/?count={variables["count"]}&search_surface={variables["search_surface"]}'
        yield response.follow(url_fer,
                              callback=self.user_followers_parse,
                              cb_kwargs={'main_user': main_user,
                                         'main_user_id': main_user_id,
                                         'variables': deepcopy(variables)},
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'})

    def user_followers_parse(self, response: HtmlResponse, main_user, main_user_id, variables):
        j_data = response.json()
        if not j_data['should_limit_list_of_followers']:
            variables["max_id"] = j_data['next_max_id']
            url_fer = f'{self.api_url}followers/?count={variables["count"]}&max_id={variables["max_id"]}\
            &search_surface={variables["search_surface"]}'
            yield response.follow(url_fer,
                                  callback=self.user_followers_parse,
                                  cb_kwargs={'main_user': main_user,
                                             'main_user_id': main_user_id,
                                             'variables': deepcopy(variables)},
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'})

        followers = j_data['users']
        for follower in followers:
            item = InstaparserItem(
                type='followers',
                main_user=main_user,
                main_user_id=main_user_id,
                user_id=follower['pk'],
                username=follower['username'],
                full_name=follower['full_name'],
                photo=follower['profile_pic_url'],
                is_private=follower['is_private']
            )
            yield item



    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        try:
            matched = re.search('{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text).group()
            return json.loads(matched).get('id')
        except:
            return re.findall('\"id\":\"\\d+\"', text)[-1].split('"')[-2]
