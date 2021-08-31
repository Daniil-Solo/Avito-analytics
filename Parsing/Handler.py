import bs4
import re
from abc import ABC, abstractmethod


class AbstractHandler(ABC):
    @abstractmethod
    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        pass


class AboutApartmentBlockHandler(AbstractHandler):
    selector = "div.item-map-location"

    def __init__(self, key_word):
        self.key_word = key_word

    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        block = soup.select_one(AboutApartmentBlockHandler.selector)
        if not block:
            text = block.text
            index_end_of_string = re.search(self.key_word, text).span()[1]
            index_end_of_line = re.search("\n", text[index_end_of_string:]).span()[0] + index_end_of_string
            data = text[index_end_of_string: index_end_of_line]
            return data
        else:
            return None


class EmptyHandler(AbstractHandler):
    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        return None


class PhysAddressHandler(AbstractHandler):
    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        geo_block = soup.select_one("div.item-map-location")
        if not geo_block:
            address = geo_block.select_one("span.item-address__string").text
            district = geo_block.select_one("span.item-address-georeferences-item__content").text
            return address + "|" + district
        else:
            return None


class NFloorsHandler(AboutApartmentBlockHandler):
    def __init__(self):
        super().__init__("Этаж:")

    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        text = super().get_info(soup)
        if text:
            index_end_srting = text.search("из", text).span()[1]
            return text[index_end_srting:]
        else:
            return None


class ApartmentFloorHandler(AbstractHandler):
    def __init__(self):
        super().__init__("Этаж:")

    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        text = super().get_info(soup)
        if text:
            index_begin_srting = text.search("из", text).span()[0]
            return text[: index_begin_srting]
        else:
            return None


class PriceHandler(AbstractHandler):
    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        price_block = soup.select_one("div.item-price-wrapper")
        if not price_block:
            price = price_block.select_one("span.js-item-price").get("content")
            return price
        else:
            return None


class TextHandler(AbstractHandler):
    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        text_block = soup.select_one("div.item-description")
        if not text_block:
            text = text_block.text
            return text
        else:
            return None


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
        elif self.key == "number of floors":
            return ApartmentFloorHandler()
        elif self.key == "price":
            return PriceHandler()
        elif self.key == "text":
            return TextHandler()
        elif self.key == "repair":
            return AboutApartmentBlockHandler("Ремонт:")
        elif self.key == "bathroom":
            return AboutApartmentBlockHandler("Санузел:")
        elif self.key == "view from the windows":
            return ViewFromWindowsHandler()
        elif self.key == "year of construction":
            return YearContructionHandler()
        elif self.key == "elevator":
            return ElevatorHandler()
        elif self.key == "garbage chute":
            return GarbageChuteHandler()
        elif self.key == "type of house":
            return TypeHouseHandler()
        elif self.key == "parking":
            return ParkingHandler()
        else:
            print("Встречен параметр, у которого отсутствует обработчик", self.key)
            return EmptyHandler()

