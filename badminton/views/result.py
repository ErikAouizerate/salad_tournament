from rest_framework.views import APIView
from badminton.services import MatchService
from django.http import JsonResponse
import json


class MatchUpView(APIView):
    def post(self, request):
        body = json.loads(request.body.decode("utf-8"))
        results = MatchService.updateResults(body)

        return JsonResponse(results, safe=False)
