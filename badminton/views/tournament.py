from rest_framework import viewsets
from badminton.models import Tournament
from badminton.serializers import TournamentSerializer, PairingsListSerializer, CompetitorSerializer
from rest_framework.decorators import action
from badminton.services import TournamentService
from rest_framework.response import Response
import json


class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

    @action(detail=True, methods=['get'])
    def nextRound(self, request, pk=None):
        tournament = self.get_object()
        tournamentService = TournamentService(tournament)
        if request.GET.get('toFinish'):
            next_round = tournamentService.pairing()
        else:
            next_round = tournamentService.pairing()

        pairingsSerialized = PairingsListSerializer(next_round['pairings'], many=True)
        benchSerialized = CompetitorSerializer(next_round['bench'], many=True)

        if request.GET.get('random'):
            tournamentService.play_random_games({"pairings": pairingsSerialized.data})

        return Response({"pairings": pairingsSerialized.data, "bench": benchSerialized.data})

    @action(detail=True, methods=['post'])
    def saveRound(self, request, pk=None):
        tournament = self.get_object()
        tournamentService = TournamentService(tournament)

        body = json.loads(request.body.decode("utf-8"))
        tournamentService.updateResults(body["round"]['results'])

        return Response({"message": f"Custom action for tournament {tournament.id}"})
