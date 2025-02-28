from rest_framework.views import APIView
from django.http import JsonResponse
from badminton.services import MatchService


class PairingView(APIView):
    def get(self, request):
        matchup = MatchService.pairing(request.GET.get('tournament'))

        if request.GET.get('random'):
            MatchService.play_games(matchup, request.GET.get('tournament'))

        return JsonResponse(matchup, safe=False)
