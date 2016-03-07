import os
import unittest
from bs4 import BeautifulSoup
from bikestats.scraper import Scraper


test_dir = os.path.abspath(os.path.dirname(__file__))


class TestScraper(unittest.TestCase):
    def test_scrape_root(self):
        with open(os.path.join(test_dir, r'http:_www.motorcyclespecs.co.za_.html')) as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            makes = list(Scraper.parse_makes(soup))
            self.assertEqual(132, len(makes))

    def test_scrape_make(self):
        with open(os.path.join(test_dir, r'http:_www.motorcyclespecs.co.za_bikes_Ducati.htm')) as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            make = Scraper.parse_make(soup)
            self.assertEqual(101, len(make))


if __name__ == '__main':
    unittest.main()
