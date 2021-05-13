from django.db import models
import jsonfield
from django.utils import timezone


class Output(models.Model):
    name = models.CharField(max_length=20)
    population_id = models.IntegerField()
    parameters = jsonfield.JSONField()
    result = jsonfield.JSONField()
    time = models.DateTimeField(default=timezone.now)


class Population(models.Model):
    name = models.CharField(max_length=20)
    individuals = jsonfield.JSONField()
    time = models.DateTimeField(default=timezone.now)


class Individual(models.Model):
    parameters = jsonfield.JSONField()
