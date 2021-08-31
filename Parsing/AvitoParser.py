import csv
import json
import requests
import bs4


class AvitoParser:
    def __init__(self):
        self.url = None
        self.file_name = None
        self.params = None
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
        with open(self.file_name, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerows(data)

    def load_new_configs(self) -> None:
        """
        This function loads configs.json and fills properties
        If there is no configs.json, file will be created with default values
        """
        try:
            with open("configs.json", 'r') as read_f:
                configs = json.load(read_f)
            self.url = configs['url']
            self.file_name = configs['file_name']
        except FileNotFoundError:
            print("Отсутствует файл configs.json")

    def start(self) -> None:
        """
        This function is main loop for collecting and saving data
        """
        n_pages = self.get_n_pages()
        if not n_pages:
            return
        for number_page in range(n_pages):
            page = Page(self.url, number_page)
            data = page.get_data(self.params)
            self.save_data(data)
