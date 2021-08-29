import csv
import json


class AvitoParser:
    def __init__(self):
        self.url = "https://www.avito.ru/perm/kvartiry"  # default value
        self.file_name = "data.csv"  # default value

    def get_n_pages(self):
        """
        This function finds out number of pages for this theme.
        This function changes self.n_page. It returns None, if some error.
        :return: number of pages
        """
        pass

    def save_data(self, data: list):
        """
        This function saves data in a file named self.file_name
        """
        with open(self.file_name, 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerows(data)

    def load_new_configs(self):
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
            configs = dict(url=self.url, file_name=self.file_name)
            with open("configs.json", 'w') as write_f:
                json.dump(configs, write_f)

    def start(self):
        """
        This function is main loop for collecting and saving data
        """
        # получение количества страниц и для каждой страницы:
        #     обращение к странице
        #     получение ссылок на объявления со страницы
        #     выполнение переход по каждой ссылке и извлечь требуемые данные
        # cохранение всех данных
