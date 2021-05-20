import json
from typing import Any

from rest_framework.response import Response
from rest_framework.views import APIView
from . import models as md
from src.population_research.simulator.species.bacteria.bacteria import Bacteria, BacteriaProperties, Genome
from src.population_research.simulator.populations.population import Population
from src.population_research.research import AvailableTypes, Research, ResearchParameters
from .models import Individual


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
            # individual_data = json.loads(individual.parameters)
            individual_data = individual.parameters
            print(individual_data)
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
            # individuals_ids = json.loads(population_data.individuals)
            new_individuals = self.get_individuals(population_data.individuals)
            new_population = Population(new_individuals, population_id)
            print(f'id {population_id}', new_population)
            Storage.put(new_population)
            return Response()
        else:
            Storage.put(Population())
            return Response(json.dumps({'id': Storage._last_id - 1}))


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
            name = request.data['name']
            population = Storage.get(token)
            for individual in population.get_all():
                individual_data = md.Individual(individual.get_parameters_dict)
                individual_data.save()
                individual.set_id(individual_data.id)
            population_data = md.Population(individuals=population.get_individual_ids, name=name)
            population_data.save()
            population.set_id(population_data.id)
        return Response()

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
        if request.method == 'POST':
            name = str(request.data['name'])
            population = Storage.get(token)
            for individual in population.get_individuals():
                individual_data = md.Individual(parameters=individual.get_parameters_dict())
                individual_data.save()
                individual.set_id(individual_data.id)
            population_data = md.Population(individuals=population.get_individual_ids(), name=name)
            population_data.save()
            output_data = md.Output(name=name, population_id=token, parameters=request['parameters'],
                                 result=request['result'])
            output_data.save()
        return Response()

    def get(self, request, token):
        Storage.delete(token)
        print(token)
        return Response('ok')


class ResearchAddIndividual(APIView):
    def post(self, request, token: str):
        print(request)
        print(request.data)
        lifetime = request.data[0]['lifetime']
        death = request.data[1]['p_for_death']
        reproduct = request.data[2]['p_for_reproduction']
        genome = Genome(lifetime, death, reproduct)
        individual_type = request.data[3]['type']
        print(individual_type)
        print(Storage._storage)
        Storage.get(token).add_individuals([AvailableTypes.get_individual(individual_type, genome)])
        return Response(json.dumps({'id': Storage._last_id - 1}))


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
