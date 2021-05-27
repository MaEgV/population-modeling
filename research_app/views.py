import json
from typing import Any
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models as md
from .research import Bacteria, BacteriaProperties, Genome
from .research.simulator import Population
from .research.research import AvailableTypes, Research, ResearchParameters, ResearchResult
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


class CreateResearch(APIView):
    @staticmethod
    def put_population(new_population: Population) -> int:
        return Storage.put(new_population)

    def get_individuals(self, individuals_ids: dict) -> list:
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

    def get(self, request, population_id=None):
        """
        Load
        Parameters
        ----------
        request
        population_id:


        Returns
        -------

        """
        print(population_id)
        if population_id is not None:
            population_data = md.Population.objects.get(pk=int(population_id))
            new_individuals = self.get_individuals(population_data.individuals)
            new_population = Population(new_individuals, population_id)
            print(f'id {population_id}', new_population)

            return Response(json.dumps({'id': Storage.put(new_population)}))
        else:

            return Response(json.dumps({'id': Storage.put(Population())}))


def save_population(population, name):
    for individual in population.get_individuals():
        individual_data = md.Individual(parameters=individual.get_parameters_dict())
        individual_data.save()
        individual.set_id(individual_data.id)

    population_data = md.Population(name=name, individuals=population.get_individual_ids())
    population_data.save()

    return population_data.id


class ResearchManage(APIView):
    def post(self, request, token: str):
        """
        Save research

        Parameters
        ----------
        request
        token

        Returns
        -------

        """
        population = Storage.get(token)
        name = request.data[0].get('name', False)

        if not name:
            return Response('Please, send a name', status=404)

        if save_population(population, name):
            return Response(status=200)

        return Response('Some problems with DB', status=404)

    def delete(self, request, token):
        Storage.delete(token)
        print(token)
        return Response('ok')


class ResearchAddIndividual(APIView):
    def post(self, request, token: str):
        print(request.data)
        lifetime = request.data['lifetime']
        death = request.data['p_for_death']
        reproduct = request.data['p_for_reproduction']
        genome = Genome(lifetime, death, reproduct)

        individual_type = request.data['type']

        Storage.get(token).add_individuals([AvailableTypes.get_individual(individual_type, genome)])

        return Response(json.dumps({'id': token}))


def save_output(population: Population, parameters: dict, output: ResearchResult, name: str):
    population_id = save_population(population, name=name)
    md.Output.objects.create(name=name,
                             population_id=population_id,
                             result=output.data.to_json(),
                             parameters=parameters)


class ResearchRun(APIView):
    def post(self, request, token: str):
        print(request.data)
        population = Storage.get(token)

        try:
            res = Research.run(population,
                               ResearchParameters(request.data['s_t'],
                                                  float(request.data['s_m']),
                                                  request.data['m_t'],
                                                  float(request.data['m_m']),
                                                  int(request.data['n'])))
        except KeyError:
            return Response('Required parameter is missed', status=404)

        name = request.data.get('name', None)
        if name:
            save_output(population, request.data, res, name)

        return Response(res.data, status=200)


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
        model = get_model_from_string(model_key)

        if model:
            return Response(get_model_table(model), status=200)
        else:
            return Response(status=404)

