import json
from typing import Any
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models as md
from src.population_research.simulator.species.bacteria.bacteria import Bacteria, BacteriaProperties, Genome
from src.population_research.simulator.populations.population import Population
from src.population_research.research import AvailableTypes, Research, ResearchParameters
import pandas as pd


class Storage:
    _storage = dict()
    _last_id = 0

    @staticmethod
    def put(item: Any):
        print(Storage._storage)
        Storage._storage[str(Storage._last_id)] = item
        Storage._last_id += 1
        return Storage._last_id - 1

    @staticmethod
    def get(key):
        return Storage._storage[key]

    @staticmethod
    def delete(key):
        del Storage._storage[key]


def get_individuals(individuals_ids: dict) -> list:
    new_individuals = list()
    for id in individuals_ids.values():
        individual = md.Individual.objects.get(pk=int(id))
        individual_data = individual.parameters
        individual_max_lifetime = individual_data['max_life_time']
        individual_p_for_death = individual_data['p_for_death']
        individual_p_for_reproduction = individual_data['p_for_reproduction']
        individual_age = individual_data['age']
        new_individuals.append(Bacteria(_properties=BacteriaProperties(_age=individual_age),
                                        _genome=Genome(individual_max_lifetime, individual_p_for_death,
                                                       individual_p_for_reproduction)))
    return new_individuals


class CreateResearch(APIView):
    def get(self, request, population_id=None):
        if population_id is not None:
            population_data = md.Population.objects.get(pk=int(population_id))
            new_individuals = get_individuals(population_data.individuals)
            new_population = Population(new_individuals, population_id)
            return Response(data=Storage.put(new_population), status=200)
        else:
            return Response(data=Storage.put(Population()), status=200)


class ResearchManage(APIView):
    def post(self, request, token: str):
        try:
            population = Storage.get(token)
        except KeyError:
            return Response(status=404)

        name = str(request.data['name'])
        for individual in population.get_individuals():
            individual_data = md.Individual(parameters=individual.get_parameters_dict())
            individual_data.save()
            individual.set_id(individual_data.id)
        md.Population.objects.create(name=name, individuals=population.get_individual_ids())

        return Response(status=200)

    def delete(self, request, token):
        try:
            Storage.delete(token)
            return Response('Population was deleted', status=200)
        except KeyError:
            return Response('No such token', status=404)



class ResearchAddIndividual(APIView):
    def post(self, request, token: str):
        lifetime = request.data['lifetime']
        death = request.data['p_for_death']
        reproduct = request.data['p_for_reproduction']
        genome = Genome(lifetime, death, reproduct)
        individual_type = request.data['type']
        Storage.get(token).add_individuals([AvailableTypes.get_individual(individual_type, genome)])
        return Response()


class ResearchRun(APIView):
    def get(self, request, token: str):
        print(request.GET)
        population = Storage.get(token)
        res = Research.run(population,
                           ResearchParameters(request.GET['s_t'],
                                              float(request.GET['s_m']),
                                              request.GET['m_t'],
                                              float(request.GET['m_m']),
                                              int(request.GET['n'])))
        return Response(res.data)


def get_model_table(model):
    table = pd.DataFrame()
    for entity in model.objects.all():
        table = table.append(entity.get_data(), ignore_index=True)

    return table


def get_model_from_string(model_key):
    if model_key == 'populations':
        return md.Population
    elif model_key == 'results':
        return md.Output


class DbManage(APIView):
    def get(self, request, model_key):
        response = Response()
        model = get_model_from_string(model_key)

        if model:
            response.data = get_model_table(model)
            response.status = 200
        else:
            response.status = 404

        return response
