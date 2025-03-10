from rest_framework import viewsets
from badminton.models import Competitor, Player, Tournament
from badminton.serializers import CompetitorSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response


class CompetitorViewSet(viewsets.ModelViewSet):
    queryset = Competitor.objects.all()
    serializer_class = CompetitorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tournament']

    def create(self, request):
        player_id = request.data.get('player_id')
        tournament_id = request.data.get('tournament_id')

        try:
            player = Player.objects.get(id=player_id)
            tournament = Tournament.objects.get(id=tournament_id)

            competitor = Competitor(
                id=player.id,
                firstname=player.firstname,
                lastname=player.lastname,
                level=player.level,
                gender=player.gender,
                tournament=tournament
            )
            competitor.save()

            serializer = self.get_serializer(competitor)
            return Response(serializer.data, status=201)
        except (Player.DoesNotExist, Tournament.DoesNotExist):
            return Response({"error": "Player or Tournament not found"}, status=404)
