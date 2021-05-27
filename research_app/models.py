from django.db import models
import jsonfield
from django.utils import timezone


class Output(models.Model):
    name = models.CharField(max_length=20)
    population_id = models.IntegerField()
    parameters = jsonfield.JSONField()
    result = jsonfield.JSONField()
    time = models.DateTimeField(default=timezone.now)

    def get_data(self):
        return {"name": self.name,
                "time": self.time,
                "population_id": self.population_id,
                "parameters": self.parameters,
                "result": self.result}


class Population(models.Model):
    name = models.CharField(max_length=20)
    individuals = jsonfield.JSONField()
    time = models.DateTimeField(default=timezone.now)

    def get_data(self):
        return {"name": self.name, "time": self.time, "info": len(self.individuals)}


class Individual(models.Model):
    parameters = jsonfield.JSONField()
