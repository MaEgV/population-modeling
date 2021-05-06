from rest_framework.response import Response
from rest_framework.views import APIView
# from src.population_research.research.population_research import Researcher

class Storage:
    _storage = dict()
    _last_id = 0

    @staticmethod
    def create_research():
        Storage._storage[Storage._last_id] = Researcher()
        Storage._last_id += 1
        print(Storage._storage)
        return Storage._last_id

    @staticmethod
    def __getitem__(self, item):
        return Storage[item]


class Research(APIView):
    def get(self, request):
        """
        wqwqeqw
        Parameters
        ----------
        request

        Returns
        -------

        """
        token = Storage.create_research()
        return Response(token)

    def update(self, request, token):
        pass

    def post(self, request):
        return Response('321')


