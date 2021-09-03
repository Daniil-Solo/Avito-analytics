import bs4
import re
from abc import ABC, abstractmethod


class AbstractHandler(ABC):
    @abstractmethod
    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        pass


class AboutApartmentBlockHandler(AbstractHandler):
    def __init__(self, key_word):
        self.key_word = key_word

    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        text = soup.text
        if re.search(self.key_word, text) is None:
            return None
        else:
            index_end_of_string = re.search(self.key_word, text).span()[1]
            index_end_of_line = re.search("\n", text[index_end_of_string:]).span()[0] + index_end_of_string
            data = text[index_end_of_string: index_end_of_line]
            data = data.replace("\xa0", " ")
            return data.strip()


class AboutHouseBlockHandler(AbstractHandler):
    def __init__(self, key_word):
        self.key_word = key_word

    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        text = soup.text
        if re.search(self.key_word, text) is None:
            return None
        else:
            index_end_of_string = re.search(self.key_word, text).span()[1]
            index_end_of_line = re.search("\n", text[index_end_of_string:]).span()[0] + index_end_of_string
            data = text[index_end_of_string: index_end_of_line]
            return data.strip()


class EmptyHandler(AbstractHandler):
    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        return None


class PhysAddressHandler(AbstractHandler):
    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        geo_block = soup.select_one("div.item-address")
        address = geo_block.text.strip().replace("\n", "|")
        return address


class NFloorsHandler(AbstractHandler):
    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        text = soup.text
        index_begin_number = re.search("/", text).span()[1]
        index_end_number = re.search(" ", text[index_begin_number:]).span()[0] + index_begin_number
        return text[index_begin_number: index_end_number]


class ApartmentFloorHandler(AbstractHandler):
    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        text = soup.text
        index_begin_number, index_end_number = re.search(r"[\d]+/", text).span()
        return text[index_begin_number: index_end_number-1]


class PriceHandler(AbstractHandler):
    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        text = soup.text
        index_begin_price = re.search("Пожаловаться", text).span()[1]
        index_end_price = re.search("₽", text[index_begin_price:]).span()[0] + index_begin_price
        price = text[index_begin_price: index_end_price]
        return re.sub(r"\D", "", price)


class Distributor:
    def __init__(self, key: str):
        self.key = key

    def distribute(self) -> AbstractHandler:
        if self.key == "physical address":
            return PhysAddressHandler()
        elif self.key == "number of rooms":
            return AboutApartmentBlockHandler("Количество комнат:")
        elif self.key == "area of apartment":
            return AboutApartmentBlockHandler("Общая площадь:")
        elif self.key == "number of floors":
            return NFloorsHandler()
        elif self.key == "apartment floor":
            return ApartmentFloorHandler()
        elif self.key == "price":
            return PriceHandler()
        elif self.key == "repair":
            return AboutApartmentBlockHandler("Ремонт:")
        elif self.key == "bathroom":
            return AboutApartmentBlockHandler("Санузел:")
        elif self.key == "view from the windows":
            return AboutApartmentBlockHandler("Вид из окон:")
        elif self.key == "terrace":
            return AboutApartmentBlockHandler("Балкон или лоджия:")
        elif self.key == "year of construction":
            return AboutHouseBlockHandler("Год постройки:")
        elif self.key == "elevator":
            return AboutHouseBlockHandler("Пассажирский лифт:")
        elif self.key == "garbage chute":
            return AboutHouseBlockHandler("В доме:")
        elif self.key == "type of house":
            return AboutApartmentBlockHandler("Тип дома:")
        elif self.key == "parking":
            return AboutApartmentBlockHandler("Парковка:")
        else:
            print("Встречен параметр, у которого отсутствует обработчик, параметр:", self.key)
            return EmptyHandler()
