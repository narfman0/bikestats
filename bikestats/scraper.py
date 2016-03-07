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
    def parse_model(soup):
        """ Parse a model of bike """
        for strip_tag in ['script', 'style']:
            for s in soup(strip_tag):
                s.extract()
        parent_element = soup.select('table[cellspacing=1]')[0]
        # gather stats
        stats = []
        for table_row in soup.select('table[cellspacing=1] tr'):
            try:
                tds = table_row.select('td')
                name = tds[0].text.strip()
                value = tds[1].text.strip()
                stats.append([name, value])
                table_row.extract()
            except:
                LOGGER.warning('Failed to parse table_row: ' + str(table_row))
        name = stats[0][1]
        # extract description
        description_element = parent_element.parent.parent.parent.parent.parent
        description = unicode(description_element).strip()
        return (name, description, stats)

    @staticmethod
    def parse_makes(soup):
        """ Parse all the makes (manufacturers) from the left bar """
        for make_anchor in soup.select('.leftMenu_container > a'):
            make = make_anchor.text.strip()
            href = make_anchor['href']
            yield [make, href]

    @staticmethod
    def parse_make(soup, recursive=False):
        """ Parse make (manufacturer) page

        Args:
            recursive: Boolean representing if each child page should also be parsed
        """
        for strip_tag in ['script', 'style']:
            for s in soup(strip_tag):
                s.extract()
        # grab models from each page
        models = list(Scraper.parse_make_models(soup))
        if recursive:
            for page in Scraper.parse_make_pages(soup):
                html = requests.get(ROOT_URL + page).text
                models.extend(Scraper.parse_make_models(BeautifulSoup(html, 'html.parser')))
        # scrape make description
        description = unicode(soup.select('div > table > tr div')[1]).replace('\r', '').replace('\t', '').strip()
        return (models, description)

    @staticmethod
    def parse_make_pages(soup):
        """ Generate list of pages, e.g. 1, 2, 3, 4 """
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
                name = anchor.text.strip().replace("\n","").replace("\r","").replace("\t","")
                href = anchor['href']
                # check if model has date information in another td
                years = -1
                if len(model_row.select('td')) > 1:
                    years = model_row.select('td')[1].text.strip().rstrip('-')
                yield [name, href, years]
            except:
                LOGGER.warning('Failed to parse model_row: ' + str(model_row))
