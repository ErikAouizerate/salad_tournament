from rest_framework.views import APIView
from django.http import JsonResponse
from badminton.services import MatchService
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class PairingView(APIView):
    @swagger_auto_schema(
        operation_description="Get pairings for a tournament",
        manual_parameters=[
            openapi.Parameter(
                'tournament',
                openapi.IN_QUERY,
                description="Tournament ID to get pairings for",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'random',
                openapi.IN_QUERY,
                description="If provided, plays random games for the matchups",
                type=openapi.TYPE_BOOLEAN,
                required=False
            ),
        ],
        responses={200: "Returns list of pairings"}
    )
    def get(self, request):
        matchup = MatchService.pairing(request.GET.get('tournament'))

        if request.GET.get('random'):
            MatchService.play_games(matchup, request.GET.get('tournament'))

        return JsonResponse(matchup, safe=False)
