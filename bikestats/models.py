from __future__ import unicode_literals

from django.db import models


class Make(models.model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    last_modified = models.DateTimeField()
    location = models.URLField()


class Stat(models.model):
    name = models.CharField(max_length=64)
    value = models.CharField(max_length=64)


class Model(models.model):
    name = models.CharField(max_length=200)
    years = models.CharField(max_length=64)
    description = models.TextField()
    stats = models.ManyToManyField(Stat)
    last_modified = models.DateTimeField()
    location = models.URLField()
