import os
import unittest
from bs4 import BeautifulSoup
from bikestats.scraper import Scraper


TEST_DIR = os.path.abspath(os.path.dirname(__file__))


class TestScraper(unittest.TestCase):
    def test_scrape_root(self):
        with open(os.path.join(TEST_DIR, r'http:_www.motorcyclespecs.co.za_.html')) as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            makes = list(Scraper.parse_makes(soup))
            self.assertEqual(132, len(makes))

    def test_scrape_make(self):
        with open(os.path.join(TEST_DIR, r'http:_www.motorcyclespecs.co.za_bikes_Ducati.htm')) as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            make = Scraper.parse_make(soup)
            self.assertEqual(101, len(make))

    def test_scrape_model(self):
        with open(os.path.join(TEST_DIR, r'http:_www.motorcyclespecs.co.za_model_ducati_ducati_monster_1200s%2015.htm')) as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            name, description, stats = Scraper.parse_model(soup)
            self.assertEqual('Ducati Monster 1200S', name)


if __name__ == '__main':
    unittest.main()
