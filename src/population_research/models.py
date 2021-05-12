from django.db import models
import jsonfield


class Input(models.Model):
    population_id = models.IntegerField()
    parameters = jsonfield.JSONField()


class Output(models.Model):
    input_id = models.IntegerField()
    result = jsonfield.JSONField()


class Population(models.Model):
    individuals = jsonfield.JSONField()


class Individual(models.Model):
    parameters = jsonfield.JSONField()
