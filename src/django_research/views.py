from typing import Any

from rest_framework.response import Response
from rest_framework.views import APIView
from src.population_research.research import Research
from src.population_research.populations.simple_population import Population


class Storage:
    _storage = dict()
    _last_id = 0

    @staticmethod
    def put(item: Any):
        Storage._last_id += 1
        Storage._storage[str(Storage._last_id)] = item
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

        return Response(Storage.put())


class ResearchManage(APIView):
    def post(self, request, token: str):
        """
        Save

        Parameters
        ----------
        request
        token

        Returns
        -------

        """

        pass

    def delete(self, request, token):
        Storage.delete(token)
        print(token)
        return Response('ok')


class ResearchAddIndividual(APIView):
    def post(self, request, token: str):
        request.data['1']
