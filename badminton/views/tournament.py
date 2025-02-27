from rest_framework import viewsets
from badminton.models import Tournament
from badminton.serializers import TournamentSerializer


class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
