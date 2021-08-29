class AvitoParser:
    def __init__(self):
        self.url = None
        self.file_name = None

    def get_n_pages(self):
        """
        This function finds out number of pages for this theme.
        This function changes self.n_page. It returns None, if some error.
        :return: number of pages
        """
        pass

    def save_data(self, data):
        """
        This function saves data in a file named self.file_name
        """
        pass

    def load_configs(self):
        """
        This function loads configs.yml and fills empty properties
        """
        pass

    def start(self):
        """
        This function is main loop for collecting and saving data
        """
        # получение количества страниц и для каждой страницы:
        #     обращение к странице
        #     получение ссылок на объявления со страницы
        #     выполнение переход по каждой ссылке и извлечь требуемые данные
        # cохранение всех данных
