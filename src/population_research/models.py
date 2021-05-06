from django.db import models
import jsonfield


# Create your models here.
class Population(models.Model):
    generations = jsonfield.JSONField()


class Generation(models.Model):
    bacterias = jsonfield.JSONField()
    parameters = jsonfield.JSONField()


class Bacteria(models.Model):
    parameters = jsonfield.JSONField()
