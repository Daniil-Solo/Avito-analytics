import unittest
import bs4
import json
from Parsing.Handler import *


def get_answers(key_word: str, right_answer: str, soup: bs4.BeautifulSoup):
    """
    This function returns values for assertEqual ('*' is required)
    It creates handler for key_word and get answer using soup
    """
    some_handle = Distributor(key_word).distribute()
    handle_answer = some_handle.get_info(soup)
    return right_answer, handle_answer


class TestHandler(unittest.TestCase):

    def test_get_right_answers_1(self):
        with open("parsing_test_1.html", 'r', encoding='utf-8') as f:
            html = f.read()
        soup = bs4.BeautifulSoup(html, "lxml")

        with open("right_answers_test_1.json", 'r', encoding='utf-8') as f:
            answers = json.load(f)

        for key in answers:
            self.assertEqual(*get_answers(key, answers[key], soup))

    def test_get_right_answers_2(self):
        with open("parsing_test_2.html", 'r', encoding='utf-8') as f:
            html = f.read()
        soup = bs4.BeautifulSoup(html, "lxml")

        with open("right_answers_test_2.json", 'r', encoding='utf-8') as f:
            answers = json.load(f)

        for key in answers:
            self.assertEqual(*get_answers(key, answers[key], soup))

    def test_get_right_answers_3(self):
        with open("parsing_test_3.html", 'r', encoding='utf-8') as f:
            html = f.read()
        soup = bs4.BeautifulSoup(html, "lxml")

        with open("right_answers_test_3.json", 'r', encoding='utf-8') as f:
            answers = json.load(f)

        for key in answers:
            self.assertEqual(*get_answers(key, answers[key], soup))
