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

    def str_to_bool(self, value):
        return value.lower() in ["true", "1", "yes", "on"] if value else False

    @action(detail=True, methods=['get'])
    def nextRound(self, request, pk=None):
        tournament = self.get_object()
        tournamentService = TournamentService(tournament)
        next_round = tournamentService.pairing()

        pairingsSerialized = PairingsListSerializer(next_round['pairings'], many=True)
        benchSerialized = CompetitorSerializer(next_round['bench'], many=True)

        if self.str_to_bool(request.GET.get('random')):
            tournamentService.play_random_games({"pairings": pairingsSerialized.data}, self.str_to_bool(request.GET.get('toFinish')))

        return Response({"pairings": pairingsSerialized.data, "bench": benchSerialized.data, "missing_rounds_after_this_one": next_round["missing_rounds"]})

    @action(detail=True, methods=['post'])
    def saveRound(self, request, pk=None):
        tournament = self.get_object()
        tournamentService = TournamentService(tournament)

        body = json.loads(request.body.decode("utf-8"))
        tournamentService.updateResults(body["round"]['results'], body['toFinish'])
        missing_rounds = tournamentService.get_missing_rounds()

        return Response({"missing_rounds": missing_rounds})

    @action(detail=True, methods=['get'])
    def missingRounds(self, request, pk=None):
        tournament = self.get_object()
        tournamentService = TournamentService(tournament)

        missing_rounds = tournamentService.get_missing_rounds()

        return Response({"missing_rounds": missing_rounds})
