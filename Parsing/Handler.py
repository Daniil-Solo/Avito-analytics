import bs4
from abc import ABC, abstractmethod


class AbstractHandler(ABC):
    @abstractmethod
    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        pass

    @abstractmethod
    def check_exists_it(self) -> bool:
        pass


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
            return None

