from rest_framework import viewsets
from badminton.models import Competitor
from badminton.serializers import CompetitorSerializer
from django_filters.rest_framework import DjangoFilterBackend


class CompetitorViewSet(viewsets.ModelViewSet):
    queryset = Competitor.objects.all()
    serializer_class = CompetitorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tournament']
