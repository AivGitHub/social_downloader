# Copyright (c) 2022, Ivan Koldakov.
# All rights reserved.
#
# Use as you want, modify as you want but please include the author's name.

from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import requests
import time


class Scraper(object):
    _BASE_SITE = 'http://vsco.co/'

    USER_INFO_HEADER = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'kX-Client-Buildeep-alive',
        'Host': 'vsco.co',
        'Referer': 'http://vsco.co/bob/images/1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }

    MEDIA_HEADER = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'vsco.co',
        'Referer': 'http://vsco.co/bob/images/1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'X-Client-Build': '1',
        'X-Client-Platform': 'web'
    }

    def __init__(self, username: str) -> None:
        self.username = username

        self.session = requests.Session()
        self.session.get(
            f'{self._BASE_SITE}content/Static/userinfo?callback=jsonp_{(str(round(time.time() * 1000)))}_0',
            headers=self.USER_INFO_HEADER
        )
        self.uid = self.session.cookies.get('vs')
        if not self.uid:
            raise ValueError('Invalid session')

        self.site_data = self.get_site_data()
        if not self.site_data.ok:
            raise ValueError(f'Invalid username `{username}`')

        self.site_data_json = self.site_data.json()
        self.site_id = self.get_site_id()

        self.media_url = f'{self._BASE_SITE}ajxp/{self.uid}/2.0/medias?site_id={self.site_id}'

    def __str__(self) -> str:
        return str(self.username)

    def get_site_data(self) -> requests.Response:
        return self.session.get(f'{self._BASE_SITE}ajxp/{self.uid}/2.0/sites?subdomain={self.username}')

    def get_site_id(self) -> str:
        return self.site_data_json['sites'][0]['id']

    def get_user_id(self) -> str:
        return self.site_data_json['sites'][0]['user_id']

    def get_media_data(self, page: int):
        media = self.session.get(self.media_url, params={'size': 100, 'page': page}, headers=self.MEDIA_HEADER)
        return media.json()['media']

    def get_images_list_by_page(self, page: int) -> list:
        _images_list = []

        page += 1
        media_data = self.get_media_data(page)
        pages_amount = len(media_data)

        _images_list.extend(media_data)

        while pages_amount > 0:
            page += 5
            media_data = self.get_media_data(page)
            pages_amount = len(media_data)

            _images_list.extend(media_data)

        return _images_list

    def get_images_list(self) -> list:
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(self.get_images_list_by_page, page): page for page in range(5)}

            for future in concurrent.futures.as_completed(future_to_url):
                data = future.result()
                return data

        return []
