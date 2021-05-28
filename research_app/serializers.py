from rest_framework import serializers
from .models import Genome, Individual

class GenomeSerializer(serializers.ModelSerializer):
    p_for_die = serializers.FloatField()
    p_for_reproduction = serializers.FloatField()
    max_lifetime = serializers.IntegerField()


class IndividualSerializer(serializers.Serializer):
    class Meta:
        model = Individual
        fields = ('id', 'type', 'genome', 'age', 'is_alive')



# class IndividualSerializer(serializers.Serializer):
#     TYPES = (('b', 'Bacteria'),)
#     type = serializers.CharField(max_length=20, choices=TYPES)
#     age = serializers.IntegerField()
#     is_alive = serializers.BooleanField()
#
#     def update(self, validated_data):
#         pass
#
#     def create(self, validated_data):
#         pass
