import unittest
import bs4
from Parsing.Handler import *


class TestPhysAddressHandler(unittest.TestCase):

    def test_get_right_address_1(self):
        with open("parsing_test_1.html", 'r', encoding='utf-8') as f:
            html = f.read()
        soup = bs4.BeautifulSoup(html, "lxml")
        handler = Distributor("physical address").distribute()
        right_answer = "Пермский край, Пермь, ул. Революции, 54| р-н Свердловский"
        self.assertEqual(handler.get_info(soup), right_answer)

    def test_get_right_address_2(self):
        with open("parsing_test_2.html", 'r', encoding='utf-8') as f:
            html = f.read()
        soup = bs4.BeautifulSoup(html, "lxml")
        handler = Distributor("physical address").distribute()
        right_answer = "ул. Гашкова, д. 51, корп. 2| р-н Мотовилихинский"
        self.assertEqual(handler.get_info(soup), right_answer)

    def test_get_right_address_3(self):
        with open("parsing_test_3.html", 'r', encoding='utf-8') as f:
            html = f.read()
        soup = bs4.BeautifulSoup(html, "lxml")
        handler = Distributor("physical address").distribute()
        right_answer = "Пермский край, Пермь, ул. Сакко и Ванцетти, 93А| р-н Мотовилихинский"
        self.assertEqual(handler.get_info(soup), right_answer)


class TestAboutApartmentBlockHandler(unittest.TestCase):
    def test_get_right_address_1(self):
        with open("parsing_test_1.html", 'r', encoding='utf-8') as f:
            html = f.read()
        soup = bs4.BeautifulSoup(html, "lxml")

        handler_area = Distributor("area of apartment").distribute()
        right_answer = "35 м²".split()[0]
        handler_answer = handler_area.get_info(soup).split()[0]
        self.assertEqual(handler_answer, right_answer)

        handler_n_rooms = Distributor("number of rooms").distribute()
        right_answer = "1"
        handler_answer = handler_n_rooms.get_info(soup)
        self.assertEqual(handler_answer, right_answer)