from __future__ import unicode_literals

import os
from bs4 import BeautifulSoup
from django.db import models

from bikestats.scraper import Scraper


class Make(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default='')
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name',)


class Model(models.Model):
    name = models.CharField(max_length=200)
    make = models.ForeignKey(Make)
    years = models.CharField(max_length=64)
    description = models.TextField(default='')
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'make', 'years')


class Stat(models.Model):
    name = models.CharField(max_length=64)
    value = models.CharField(max_length=64)
    model = models.ForeignKey(Model)

    class Meta:
        unique_together = ('name', 'model')


def parse_all(scraped_root_path):
    """ Parse all bike information and stick in database. Current naive-mode *shrugs*

    Args:
        scraped_root_path: Path to the scraped directory of the website
    """
    soup = BeautifulSoup(open(os.path.join(scraped_root_path, 'index.html')).read(), "html.parser")
    for name, make_href in Scraper.parse_makes(soup):
        make = Make.objects.get_or_create(name=name)
        make_soup = BeautifulSoup(open(os.path.join(scraped_root_path, make_href)).read(), "html.parser")
        models, description_make, pages = Scraper.parse_make(make_soup)
        for page in pages:
            page_soup = BeautifulSoup(open(os.path.join(scraped_root_path, page)).read(), "html.parser")
            _models, _d, _p = Scraper.parse_make(page_soup)
            models.extend(_models)
        for name_model, model_href, years in models:
            model = Model.get_or_create(name=name_model, make=make, years=years)
            model_soup = BeautifulSoup(open(os.path.join(scraped_root_path, 'bikes', model_href)).read(), "html.parser")
            name_model_2, description_model, stats = Scraper.parse_model(model_soup)
            for name, value in stats:
                Stat.get_or_create(name=name, value=value, model=model)
