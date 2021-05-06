from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.views import APIView

from .research.parameters import IndividualParameters
from .research.population_research import Researcher


class Storage:
    _storage = dict()
    _last_id = 0

    @staticmethod
    def create_research():
        Storage._storage[str(Storage._last_id)] = Researcher()
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
    def get(self, request):
        print(request)
        #redirect(f'research/{Storage.create_research()}')
        return Response(Storage.create_research())


class ManageResearch(APIView):
    def post(self, request, token: str, action):
        print(request.data, token, action)
        method = getattr(Storage.get(token), action)
        method(IndividualParameters('bacteria', 4, 0.5, 0.5))
        #species, lifetime, p_for_death, p_for_repr = request.POST['s'], request.POST['l'], request.POST['p1'], request.POST['p2'],
        #print(species, lifetime, p_for_death, p_for_repr)
        #Storage.get(str(token)).add_individual(IndividualParameters('bacteria', 4, 0.5, 0.5))
        return Response('ok')

    def delete(self, request, token):
        Storage.delete(token)
        print(token)
        return Response(request.data)
