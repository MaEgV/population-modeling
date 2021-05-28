import json
from typing import Any

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models as md
from .research import Bacteria, BacteriaProperties, Genome
from .research.simulator import Population, AbstractSpecies
from .research.research import AvailableTypes, Research, ResearchParameters, ResearchResult
import pandas as pd


class Storage:
    """
    Static class with the hidden storage
    That is RAM - storage off application
    Elements can only be accessed by a key generated by the Storage class

    Attributes
    ----------
    _storage: dict:
        dict with stored items
    _last_id: int
        inner counter of items

    Methods
    -------
    put(item: Any) -> Any:
        put item to Storage and return its key
    get(key: Any) -> Any:
        return item from Storage by key request
    delete(key: Any) -> None:
        delete item by key
    """
    _storage = dict()
    _last_id = 0

    @staticmethod
    def put(item: Any) -> Any:
        print(Storage._storage)
        Storage._storage[str(Storage._last_id)] = item
        Storage._last_id += 1
        return Storage._last_id - 1

    @staticmethod
    def get(key: Any) -> Any:
        return Storage._storage[key]

    @staticmethod
    def delete(key: Any) -> None:
        del Storage._storage[key]


def get_individuals(individuals: Any) -> list:
    new_individuals = list()
    for individual_dict in individuals.values():
        genome = md.Genome.objects.get(pk=individual_dict['genome_id'])
        print(genome)
        individual_max_lifetime = genome.max_lifetime
        individual_p_for_death = genome.p_for_die
        individual_p_for_reproduction = genome.p_for_reproduction
        individual_age = individual_dict['age']
        new_individuals.append(Bacteria(_properties=BacteriaProperties(_age=individual_age),
                                        _genome=Genome(individual_max_lifetime, individual_p_for_death,
                                                       individual_p_for_reproduction)))
    return new_individuals


class CreateResearch(APIView):
    """
    Implementation of creation of research and its saving in storage

    Attributes
    ----------
    _storage: dict:
        dict with stored items
    _last_id: int
        inner counter of items

    Methods
    -------
    get(self, request: Request, population_id=None) -> Response:
        REST method (GET) which create Population, or load it from DB to RAM
    """
    def get(self, request: Request, population_id: str = None) -> Response:
        """
        Create Population and save it in Storage

        Parameters
        ----------
        request: Request:
            request from client
        population_id: int:
            id from DB of needed population

        Returns
        -------
            Response with token from Storage for next accesses
        """
        if population_id is not None:
            population_data = md.Population.objects.get(pk=int(population_id))
            loaded_individuals = get_individuals(population_data.individuals.all())
            loaded_population = Population(loaded_individuals)
            return Response(json.dumps({'id': Storage.put(loaded_population)}))
        else:
            return Response(json.dumps({'id': Storage.put(Population())}))


def save_genome(genome_dict: dict) -> md.Genome:
    genome_data = md.Genome(p_for_die=genome_dict['p_for_death'],
                            p_for_reproduction=genome_dict['p_for_reproduction'],
                            max_lifetime=genome_dict['max_life_time'])
    genome_data.save()
    return genome_data


def save_individual(individual: AbstractSpecies) -> md.Individual:
    individual_data = md.Individual(**(individual.get_state_dict()),
                                    genome=save_genome(individual.get_genome_dict()),
                                    type=md.Individual.type_to_str(individual))
    individual_data.save()
    return individual_data


def save_population(population: Population, name: str) -> int:
    """
    Function which save python instance of Population to BD
    Parameters
    ----------
    population: Population:
        to save
    name: str:
        name of saving data

    Returns
    -------
        id of new item from DB
    """
    population_data = md.Population(name=name)
    population_data.save()

    for individual in population.get_individuals():
        population_data.individuals.add(save_individual(individual))

    return population_data.id


class PopulationManage(APIView):
    """
    Manager of Populations to RAM(Storage)
    Possible actions:
    save Population to DB
    delete from RAM

    Methods
    -------
    post(self, request: Request, token: str) -> Response:
    REST method(POST) to save Population
    """

    def post(self, request: Request, token: str) -> Response:
        """
        Save Population associated with key to DB
        Parameters
        ----------
        request:
            client request
        token:
            key from storage

        Returns
        -------

        """
        population = Storage.get(token)
        name = request.data.get('name', False)

        if not name:
            return Response('Please, send a name', status=404)
        else:
            key = save_population(population, name)
            return Response(f"Population was saved with id:{key}", status=200)

    def delete(self, request: Request, token: str) -> Response:
        """
        Delete Population associated with key
        Parameters
        ----------
        request:
            client request
        token:
            key from DB
        """
        Storage.delete(token)
        return Response('ok')


class AddIndividual(APIView):
    """
    Add individual to Population associated with key
    Parameters
    """
    def post(self, request: Request, token: str) -> Response:
        """
        Add individual to Population associated with key
        Parameters
        ----------
        request:
            client request
        token:
            key

        Returns
        -------

        """
        genome = Genome(request.data['lifetime'],
                        request.data['p_for_death'],
                        request.data['p_for_reproduction'])

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
    """
    Build research with Population
    """
    def post(self, request: Request, token: str)->Response:
        """
        Build research posted parameters and population associated with key
        Parameters
        ----------
        request:
            client request
        token:
            key from Storage
        Returns
        -------

        """
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


def get_model_table(model: Any) -> pd.DataFrame:
    table = pd.DataFrame()
    for entity in model.objects.all():
        table = table.append(entity.get_data(), ignore_index=True)

    return table


def get_model_from_string(model_key: str)->Any:
    if model_key == 'populations':
        return md.Population
    elif model_key == 'results':
        return md.Output


class DbManage(APIView):
    """
    Class that gives access to DB tables
    """
    def get(self, request, model_key):
        """

        Parameters
        ----------
        request:
            client request
        model_key:
            name of needed table

        Returns
        -------
            Json with data from DB
        """
        model = get_model_from_string(model_key)

        if model:
            return Response(get_model_table(model), status=200)
        else:
            return Response(status=404)
