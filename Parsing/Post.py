import bs4
import requests


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
        soup = bs4.BeautifulSoup(html, "lxml")

        key_storage = dict()
        for key in params:
            if params[key]:
                key_storage[key] = ""
                handler = Distributor(key).distribute()
                key_storage[key] = handler.get_data()
        return list(key_storage.values())
