import time
import bs4
import requests

from Parsing.Post import Post


class Page:
    def __init__(self, url, page_number):
        self.url = url
        self.p_num = page_number

    def get_urls(self) -> list:
        """
        This function returns list of urls on apartments
        It uses self.url and self.p_num for creating request
        If there is connection error, it returns []
        """
        try:
            request = requests.get(self.url, params=dict(p=self.p_num))
            html = request.text
            soup = bs4.BeautifulSoup(html, "lxml")
            blocks = soup.select("div.iva-item-content-UnQQ4")
            urls = []
            for block in blocks:
                url = block.select_one('div.iva-item-titleStep-_CxvN').select_one('a').get('href')
                urls.append(url)
            return urls
        except requests.exceptions.ConnectionError:
            print("Отсутствует соединение")
            return []

    def get_data(self, params: dict) -> list:
        """
        This function returns list of data about apartments
        If there is connection error, it returns []
        """
        urls = self.get_urls()
        data = []
        for url in urls:
            post = Post(url)
            data.append(post.get_data(params))
            time.sleep(5)
        return data
