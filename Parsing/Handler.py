import bs4
import re
from abc import ABC, abstractmethod


class AbstractHandler(ABC):
    @abstractmethod
    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        pass


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


class NRoomsHandler(AbstractHandler):
    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        geo_block = soup.select_one("div.item-params")
        if not geo_block:
            text = geo_block.text
            index_end_of_string = re.search("Количество комнат:", text).span()[1]
            index_end_of_line = re.search("\n", text[index_end_of_string:]).span()[0] + index_end_of_string
            n_rooms = text[index_end_of_string: index_end_of_line]
            return n_rooms
        else:
            return None


class AreaAppartmentHandler(AbstractHandler):
    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        geo_block = soup.select_one("div.item-params")
        if not geo_block:
            text = geo_block.text
            index_end_of_string = re.search("Общая площадь:", text).span()[1]
            index_end_of_line = re.search("\n", text[index_end_of_string:]).span()[0] + index_end_of_string
            area = text[index_end_of_string: index_end_of_line]
            return area
        else:
            return None


class NFloorsHandler(AbstractHandler):
    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        geo_block = soup.select_one("div.item-params")
        if not geo_block:
            text = geo_block.text
            index_end_of_string = re.search("Этаж: ", text).span()[1]
            index_end_of_line = re.search("\n", text[index_end_of_string:]).span()[0] + index_end_of_string
            index_end_this_floor = re.search("из", text[index_end_of_string:]).span()[1] + index_end_of_string
            area = text[index_end_this_floor: index_end_of_line]
            return area
        else:
            return None


class Distributor:
    def __init__(self, key: str):
        self.key = key

    def distribute(self) -> AbstractHandler:
        if self.key == "physical address":
            return PhysAddressHandler()
        elif self.key == "number of rooms":
            return NRoomsHandler()
        elif self.key == "area of apartment":
            return AreaAppartmentHandler()
        elif self.key == "number of floors":
            return NFloorsHandler()
        elif self.key == "number of floors":
            return AppartmentFloorHandler()
        elif self.key == "price":
            return PriceHandler()
        elif self.key == "text":
            return TextHandler()
        elif self.key == "repair":
            return RepairHandler()
        elif self.key == "bathroom":
            return BathroomHandler()
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

