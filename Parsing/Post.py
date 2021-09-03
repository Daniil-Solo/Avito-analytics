from bs4 import BeautifulSoup
import requests

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
        print(full_url)
        if request.reason != 'OK':
            print("Возникла ошибка", request.reason)
        html = request.text
        soup = BeautifulSoup(html, "lxml")
        key_storage = dict()
        for key in [key for key in params if params[key]]:
            if key == "link":
                key_storage[key] = full_url
            else:
                handler = Distributor(key).distribute()
                try:
                    key_storage[key] = handler.get_info(soup)
                except AttributeError or TypeError:
                    key_storage[key] = None
        return list(key_storage.values())
