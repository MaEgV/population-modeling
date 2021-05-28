from django.db import models
import jsonfield
from django.utils import timezone

from research_app.research import Bacteria
from research_app.research.simulator import AbstractSpecies


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


class Genome(models.Model):
    p_for_die = models.FloatField()
    p_for_reproduction = models.FloatField()
    max_lifetime = models.IntegerField()


class Individual(models.Model):
    TYPES = (('b', 'bacteria'),)
    type = models.CharField(max_length=20, choices=TYPES, default=None)
    genome = models.OneToOneField(Genome, on_delete=models.CASCADE, default=None)
    age = models.IntegerField(default=0)
    is_alive = models.BooleanField(default=None)

    @staticmethod
    def type_to_str(individual: AbstractSpecies):
        if type(individual) == Bacteria:
            return 'b'


class Population(models.Model):
    name = models.CharField(max_length=20)
    individuals = models.ManyToManyField(Individual)
    time = models.DateTimeField(default=timezone.now)

    def get_data(self):
        return {"name": self.name, "time": self.time, "info": len(self.individuals)}
