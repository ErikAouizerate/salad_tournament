from rest_framework import viewsets
from badminton.models import Player
from badminton.serializers import PlayerSerializer
from django_filters.rest_framework import DjangoFilterBackend


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tournament']
