import csv
import time
import json
import requests
import bs4

from Parsing.Page import Page


class AvitoParser:
    LOOP_DELAY = 5

    def __init__(self):
        self.url = None
        self.file_name = None
        self.params = None
        self.has_headers = False
        self.load_new_configs()

    def get_n_pages(self) -> int or None:
        """
        This function finds out number of pages for this theme.
        It returns None, if some error.
        :return: number of pages or None
        """
        try:
            request = requests.get(self.url)
            html = request.text
            soup = bs4.BeautifulSoup(html, "lxml")
            list_page_buttons = soup.select_one("div.pagination-root-Ntd_O").select('span')
            max_number_page = list_page_buttons[-2].text
            return int(max_number_page)
        except requests.exceptions.ConnectionError:
            print("Отсутствует соединение")
            return None

    def save_data(self, data: list) -> None:
        """
        This function saves data in a file named self.file_name
        """
        print("Сохранение")
        if not self.has_headers:
            headers = [key for key in self.params if self.params[key]]
            with open(self.file_name, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file, delimiter=';')
                writer.writerow(headers)
            self.has_headers = True

        with open(self.file_name, 'a', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerows(data)

    def load_new_configs(self) -> None:
        """
        This function loads configs.json and fills properties
        If there is no configs.json, file will be created with default values
        """
        try:
            with open("Parsing/configs.json", 'r') as read_f:
                configs = json.load(read_f)
            self.url = configs['url']
            self.file_name = configs['file_name']
            self.params = configs['params']
        except FileNotFoundError:
            print("Отсутствует файл configs.json")

    def start(self) -> None:
        """
        This function is main loop for collecting and saving data
        """
        n_pages = range(self.get_n_pages())
        if not n_pages:
            return
        for number_page in n_pages:
            page = Page(self.url, number_page)
            data = page.get_data(self.params)
            if not data:
                return
            self.save_data(data)
            time.sleep(AvitoParser.LOOP_DELAY)
