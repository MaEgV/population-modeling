from rest_framework.response import Response
from rest_framework.views import APIView
from src.population_research.research import Research
from django.http import HttpResponse
from .models import Output, Population, Individual


class Storage:
    _storage = dict()
    _last_id = 0

    @staticmethod
    def create_research(research: Research = None):
        new_research = research if research else Research()
        Storage._storage[str(Storage._last_id)] = new_research
        Storage._last_id += 1
        print(Storage._storage)
        return Storage._last_id - 1

    @staticmethod
    def get(key):
        return Storage._storage[key]

    @staticmethod
    def delete(key):
        del Storage._storage[key]


class CreateResearch(APIView):
    def get(self, request, id=None):
        """
        Load
        Parameters
        ----------
        request
        id

        Returns
        -------

        """
        print(request)

        return Response(Storage.create_research())


class ResearchManage(APIView):

    def post(self, request, token: str):
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
            population = Storage.get(population_token)
            population_data = Population(individuals=population.get_individual_ids)
            population_data.save()
            for individual in population.get_all():
                individual_data = Individual(individual.get_genome_dict)
                individual_data.save()


    def delete(self, request, token):
        Storage.delete(token)
        print(token)
        return Response('ok')


class ResearchAddIndividual(APIView):
    def post(self, request, token: str):
        request.data
