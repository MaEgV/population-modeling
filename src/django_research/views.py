import json
from typing import Any

from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Output, Population, Individual
from src.population_research.simulator.species.bacteria.bacteria import Bacteria, BacteriaProperties, Genome
from src.population_research.simulator.populations import population


class Storage:
    _storage = dict()
    _last_id = 0

    @staticmethod
    def put(item: Any):
        Storage._storage[str(Storage._last_id)] = item
        print(Storage._storage)
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
            individual = Individual.objects.get(pk=int(id))
            individual_data = json.loads(individual['parameters'])
            individual_max_lifetime = individual_data['max_lifetime']
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
        if request.method == 'GET':

            if population_id:
                population_data = Population.objects.get(pk=population_id)
                individuals_ids = json.loads(population_data['individuals'])
                new_individuals = self.get_individuals(individuals_ids)
                new_population = Population(new_individuals, population_id)
                return Response(self.put_population(new_population))
            else:
                return Response(self.put_population(population.Population()))


class ResearchManage(APIView):

    # def post(self, request, token: str):
    #     """
    #     Save population
    #
    #     Parameters
    #     ----------
    #     request
    #     token
    #
    #     Returns
    #     -------
    #
    #     """
    #     if request.method == 'POST':
    #         name = request.data['name']
    #         population = Storage.get(token)
    #         population_data = Population(individuals=population.get_individual_ids, name=name)
    #         population_data.save()
    #         for individual in population.get_all():
    #             individual_data = Individual(individual.get_parameters_dict)
    #             individual_data.save()
    #     return Response()

    def post(self, request, token: str):
        """
        Save researcher

        Parameters
        ----------
        request
        token

        Returns
        -------

        """
        if request.method == 'POST':
            name = request.data['name']
            population = Storage.get(token)
            population_data = Population(individuals=population.get_individual_ids, name=name)
            population_data.save()
            for individual in population.get_individuals():
                individual_data = Individual(individual.get_parameters_dict)
                individual_data.save()
            output_data = Output(name=name, population_id=token, parameters=request['parameters'],
                                 result=request['result'])
            output_data.save()
        return Response()


    def delete(self, request, token):
        Storage.delete(token)
        print(token)
        return Response('ok')


class ResearchAddIndividual(APIView):
    def post(self, request, token: str):
        print(request.data)
        return Response()


class ResearchRun(APIView):
    def get(self, request, token: str):
        print(request)
        print(request.GET)
        return Response()
