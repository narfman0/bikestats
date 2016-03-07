import logging
import re
import requests
from bs4 import BeautifulSoup


LOGGER = logging.getLogger(__name__)
ROOT_URL = 'http://www.motorcyclespecs.co.za/'


class Scraper(object):
    """ We scrape the website and store the information in the models. We save the urls
    and the previously modified time, so that if anything is updated, we may update our
    resources. We also don't want to peg the site too much, by being good webizens. """
    @staticmethod
    def parse_makes(soup):
        """ Parse all the makes (manufacturers) from the left bar """
        for make_anchor in soup.select('.leftMenu_container > a'):
            make = Scraper.get_text(make_anchor)
            href = make_anchor['href']
            yield [make, href]

    @staticmethod
    def parse_make(soup, recursive=False):
        """ Parse make (manufacturer) page

        Args:
            recursive: Boolean representing if each child page should also be parsed
        """
        # grab models from each page
        models = list(Scraper.parse_make_models(soup))
        if recursive:
            for page in Scraper.parse_make_pages(soup):
                html = requests.get(ROOT_URL + page).text
                models.extend(Scraper.parse_make_models(BeautifulSoup(html, 'html.parser')))
        # scrape make description
        return models

    @staticmethod
    def parse_make_pages(soup):
        # generate list of pages, e.g. 1, 2, 3, 4
        pages = []
        for anchor in soup.select('p > font > a'):
            href = anchor['href']
            if 'model' not in href:
                pages.append(href)
        return set(pages)

    @staticmethod
    def parse_make_models(soup):
        """ Parse all the make's models on a given page. """
        for model_row in soup.select('div > table > tr div > table > tr'):
            try:
                anchor = model_row.select('a')[0]
                name = Scraper.get_text(anchor).strip()
                href = anchor['href']
                # check if model has date information in another td
                years = -1
                if len(model_row.select('td')) > 1:
                    years = model_row.select('td')[1].text.strip().rstrip('-')
                yield [name, href, years]
            except:
                LOGGER.warning('Failed to parse model_row: ' + str(model_row))

    @staticmethod
    def get_text(item):
        """ Non-recursively extract text from an item """
        return item.find(text=True, recursive=False).strip()
