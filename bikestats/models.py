from __future__ import unicode_literals

import requests
from bs4 import BeautifulSoup
from django.db import models

from bikestats.scraper import Scraper


class Make(models.model):
    name = models.CharField(max_length=200)
    description = models.TextField(default='')
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        unique_together = ('name')


class Model(models.model):
    name = models.CharField(max_length=200)
    make = models.ForeignKey(Make)
    years = models.CharField(max_length=64)
    description = models.TextField(default='')
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        unique_together = ('name', 'make', 'years')


class Stat(models.model):
    name = models.CharField(max_length=64)
    value = models.CharField(max_length=64)
    model = models.ForeignKey(Model)

    class Meta:
        unique_together = ('name', 'model')


def parse_all():
    """ Parse all bike information and stick in database. Current naive-mode *shrugs* """
    soup = BeautifulSoup(requests.get(ROOT_URL).text, "html.parser")
    for name, make_href in Scraper.parse_makes(soup):
        make = Make.objects.get_or_create(name=name)
        make_soup = BeautifulSoup(requests.get(ROOT_URL + make_href).text, "html.parser")
        models, description_make = Scraper.parse_make(make_soup, True)
        for name_model, model_href, years in models:
            model = Model.get_or_create(name=name_model, make=make, years=years)
            model_soup = BeautifulSoup(requests.get(ROOT_URL + model_href).text, "html.parser")
            name_model_2, description_model, stats = Scraper.parse_model(model_soup)
            for name, value in stats:
                Stat.get_or_create(name=name, value=value, model=model)
