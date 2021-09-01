from bs4 import BeautifulSoup
import requests
import re

from Parsing.Handler import Distributor


class Post:
    domain = "https://www.avito.ru"

    def __init__(self, short_url):
        self.short_url = short_url

    def get_data(self, params: dict) -> list:
        """
        This function returns data of one apartments
        It uses parameters from params
        Connection error will be handle on class Page
        """
        full_url = Post.domain + self.short_url
        request = requests.get(full_url)
        html = request.text
        soup = BeautifulSoup(html, "lxml")
        key_storage = dict(link=full_url)
        params_without_link = params.copy()
        params_without_link.pop("link")
        for key in params_without_link:
            if params[key]:
                key_storage[key] = ""
                handler = Distributor(key).distribute()
                try:
                    key_storage[key] = self.clear(handler.get_info(soup))
                except AttributeError or TypeError:
                    key_storage[key] = None
        return list(key_storage.values())

    @staticmethod
    def clear(dirty_data: str) -> str:
        """
        This function returns clear data
        Output data contains only russian letters, some punctuations
        """
        data = re.sub("\n", " ", dirty_data)
        data = re.findall(r"[А-Яа-я\d .,-]+", data)
        data = [item.strip() for item in data]
        data = ''.join(data)
        return data
