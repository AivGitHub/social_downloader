# Copyright (c) 2022, Ivan Koldakov.
# All rights reserved.
#
# Use as you want, modify as you want but please include the author's name.

import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import pathlib
import pprint
import sys
from typing import Optional

import requests

from vsco.scraper import Scraper as ScraperVSCO


class Maintain(object):
    _DEFAULT_CHUNK_SIZE = 1024 * 1024
    _PROTOCOL = 'http://'
    __NO_ARGS_PATH = 'downloaded_data'

    def __init__(self, **kwargs) -> None:
        """ TODO: Update to setter if needed

        :param kwargs: user arguments
        """

        _data = kwargs.get('data')
        _usernames_arg = _data.split() if _data else kwargs.get('usernames')

        assert _usernames_arg != [], 'Usernames is an required argument'

        # TODO: in the future it should be a required field.
        self.network = kwargs.get('network') or 'vsco'

        self.usernames = _usernames_arg
        self.quiet = kwargs.get('quiet')
        self.mode = kwargs.get('mode')

        self.path_to_save = kwargs.get('path')

    def __str__(self) -> str:
        return str('_'.join(self.usernames))

    @property
    def path_to_save(self) -> pathlib.Path:
        return self.__path_to_save

    @path_to_save.setter
    def path_to_save(self, _path: list) -> None:
        """ TODO: Ask if path exists and user want's to merge directories

        :param _path: Path to set
        :return: None
        """

        if _path and _path[0]:
            self.__path_to_save = (pathlib.Path(_path[0]) / self.network).resolve()
        else:
            self.__path_to_save = (pathlib.Path.cwd() / self.__NO_ARGS_PATH / self.network).resolve()

    def download_video(self, data: dict, username: Optional[str] = None) -> None:
        """ Can be used independently (without download_media)

        :param data: dict with media data
        :param username: username of a downloading person
        :return: None
        """

        _video_url = data.get('video_url')
        _file_name = _video_url.split('/')[-1]

        if not username:
            username = data.get('perma_subdomain')

        _video_container_path = self.path_to_save / username / 'video'
        _file_path = _video_container_path / _file_name

        _video_container_path.mkdir(parents=True, exist_ok=True)

        link = f'{self._PROTOCOL}{_video_url}'

        with _file_path.open('wb') as f:
            for chunk in requests.get(link, stream=True).iter_content(chunk_size=self._DEFAULT_CHUNK_SIZE):
                f.write(chunk)

    def download_image(self, data: dict, username: Optional[str] = None) -> None:
        """ Can be used independently (without download_media)

        :param data: dict with media data
        :param username: username of a downloading person
        :return: None
        """

        _responsive_url = data.get('responsive_url')
        _file_name = _responsive_url.split('/')[-1]

        if not username:
            username = data.get('perma_subdomain')

        _image_container_path = self.path_to_save / username / 'images'
        _file_path = _image_container_path / _file_name

        _image_container_path.mkdir(parents=True, exist_ok=True)

        link = f'{self._PROTOCOL}{_responsive_url}'

        _file_path.write_bytes(requests.get(link, stream=True).content)

    def download_media(self, data: dict, username: Optional[str] = None) -> None:
        """

        :param data: dict with media data
        :param username: username of a downloading person
        :return: None
        """

        _username_path = self.path_to_save / username
        is_video = data.get('is_video')

        if not username:
            username = data.get('perma_subdomain')

        _username_path.mkdir(parents=True, exist_ok=True)

        if is_video:
            self.download_video(data, username=username)
        else:
            self.download_image(data, username=username)

    def process(self) -> None:
        self.std(f'Started {self.mode} process..')

        # TODO: Parallel
        for username in self.usernames:
            self.std('processing %s' % username)

            if self.network == 'vsco':
                scraper = ScraperVSCO(username)
            else:
                raise NotImplementedError(f'Network {self.network} does not support!')

            _images_list = scraper.get_images_list()
            _username_path = self.path_to_save / username
            _information_file = self.path_to_save / username / 'information.txt'

            _username_path.mkdir(parents=True, exist_ok=True)

            _information_file.write_text(pprint.pformat(scraper.site_data_json))

            with ThreadPoolExecutor(max_workers=5) as executor:
                future_to_url = {
                    executor.submit(self.download_media, _data, username=username): _data for _data in _images_list
                }

                for future in concurrent.futures.as_completed(future_to_url):
                    future.result()

    def std(self, message, to_err=False) -> None:
        if self.quiet:
            return

        out = sys.stderr if to_err else sys.stdout
        out.write(str(message))
        out.write('\n')

        out.flush()
