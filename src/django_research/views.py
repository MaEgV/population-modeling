import json
from typing import Any
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models as md
from src.population_research.simulator.species.bacteria.bacteria import Bacteria, BacteriaProperties, Genome
from src.population_research.simulator.populations.population import Population
from src.population_research.research import AvailableTypes, Research, ResearchParameters


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
    def get_individuals(self, individuals_ids: dict) -> list:
        new_individuals = list()
        for id in individuals_ids.values():
            individual = md.Individual.objects.get(pk=int(id))
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
        print(request.data)
        if request.method == 'GET':
            if population_id is not None:
                population_data = md.Population.objects.get(pk=population_id)
                individuals_ids = json.loads(population_data['individuals'])
                new_individuals = self.get_individuals(individuals_ids)
                new_population = Population(new_individuals, population_id)
                print(f'id {population_id}', new_population)
                return Response(Storage.put(new_population))
            else:
                return Response(Storage.put(Population()))


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
        if request.method == 'POST':
            name = str(request.data['name'])
            population = Storage.get(token)
            for individual in population.get_individuals():
                individual_data = md.Individual(individual.get_parameters_dict())
                individual_data.save()
                individual.set_id(individual_data.id)
            population_data = md.Population(individuals=population.get_individual_ids(), name=name)
            population_data.save()
            # for individual in population.get_all():
            #     individual_data = md.Individual(individual.get_parameters_dict)
            #     individual_data.save()
            # output_data = md.Output(name=name, population_id=token, parameters=request['parameters'],
            #                      result=request['result'])
            # output_data.save()
        return Response()

    def delete(self, request, token):
        Storage.delete(token)
        print(token)
        return Response('ok')


class ResearchAddIndividual(APIView):
    def post(self, request, token: str):
        print(request.data)
        genome = Genome(request.data['lt'], request.data['p_d'], request.data['p_r'])
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
