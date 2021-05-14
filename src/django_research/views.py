import json
from typing import Any

from rest_framework.response import Response
from rest_framework.views import APIView
from src.population_research.research import Research
from django.http import HttpResponse
from .models import Output, Population, Individual
from src.population_research.species.bacteria.bacteria import Bacteria, BacteriaProperties, Genome
from src.population_research.populations import simple_population


class Storage:
    _storage = dict()
    _last_id = 0

    @staticmethod
    def put(item: Any):
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
    def get_population(self, request, id=None):
        """
        Load
        Parameters
        ----------
        request
        id

        Returns
        -------

        """
        if request.method == 'GET':
            if id:
                new_individuals = list()
                population_token = request['token']
                population_data = Population.objects.get(pk=population_token)
                individuals_ids = json.loads(population_data['individuals'])
                for id in individuals_ids.values():
                    individual = Individual.objects.get(pk=id)
                    individual_data = json.loads(individual['parameters'])
                    individual_max_lifetime = individual_data['max_lifetime']
                    individual_p_for_death = individual_data['p_for_death']
                    individual_p_for_reproduction = individual_data['p_for_reproduction']
                    individual_age = individual_data['age']
                    new_individuals.append(Bacteria(_properties=BacteriaProperties(_age=individual_age),
                                                    _genome=Genome(individual_max_lifetime, individual_p_for_death,
                                                                   individual_p_for_reproduction)))
                    new_population = Population(new_individuals, population_token)
                return new_population
            else:
                new_population = simple_population.Population()
                token = Storage.put(new_population)
                return Response(token)
        # print(request)
        #
        # return Response(Storage.create_research())

    def get_results(self, request):
        """

        :param request:
        :return:
        """
        if request.method == 'GET':
            token = request['token']
            research_data = Output.objects.get(pk=token)
            return research_data['result']



class ResearchManage(APIView):

    def post_population(self, request, token: str):
        """
        Save population

        Parameters
        ----------
        request
        token

        Returns
        -------

        """
        if request.method == 'POST':
            population_token = request['token']
            name = request['name']
            population = Storage.get(population_token)
            population_data = Population(individuals=population.get_individual_ids, name=name)
            population_data.save()
            for individual in population.get_all():
                individual_data = Individual(individual.get_parameters_dict)
                individual_data.save()

    def post_research(self, request, token: str):
        """
        Save research

        Parameters
        ----------
        request
        token

        Returns
        -------

        """
        if request.method == 'POST':
            population_token = request['token']
            name = request['name']
            population = Storage.get(population_token)
            population_data = Population(individuals=population.get_individual_ids, name=name)
            population_data.save()
            for individual in population.get_all():
                individual_data = Individual(individual.get_parameters_dict)
                individual_data.save()
            output_data = Output(name=name, population_id=population_token, parameters=request['parameters'],
                                 result=request['result'])
            output_data.save()


    def delete(self, request, token):
        Storage.delete(token)
        print(token)
        return Response('ok')


class ResearchAddIndividual(APIView):
    def post(self, request, token: str):
        request.data
