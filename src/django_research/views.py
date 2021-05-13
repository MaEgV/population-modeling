import json

from rest_framework.response import Response
from rest_framework.views import APIView
from src.population_research.research import Research
from django.http import HttpResponse
from .models import Output, Population, Individual
from src.population_research.species.bacteria.bacteria import Bacteria, BacteriaProperties, Genome
from src.population_research.populations.simple_population import Population


class Storage:
    _storage = dict()
    _last_id = 0

    @staticmethod
    def create_research(research: Research = None):
        new_research = research if research else Research()
        Storage._storage[str(Storage._last_id)] = new_research
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
            new_individuals = list()
            population_token = request['token']
            poplation_data = Population.objects.get(pk=population_token)
            individuals_ids = json.loads(poplation_data['individuals'])
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
