from rest_framework import serializers
from badminton.models import Player


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'firstname', 'lastname', 'won', 'played', 'level', 'rank']
