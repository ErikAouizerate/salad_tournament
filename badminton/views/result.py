from rest_framework.views import APIView
from .models import Player, Tournament, Partner
import statistics
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
import random
from django.db.models.functions import Random
from django.db.models import Case, When


class ModelEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if hasattr(obj, '_meta'):
            return {
                'id': obj.id,
                'str': str(obj),
            }


class MatchUpView(APIView):
    def updateResults(self, matchup):
        results = []
        for match in matchup:
            is_won = bool(random.getrandbits(1))
            a = match["first"]["a"]["id"]
            b = match["first"]["b"]["id"]
            c = match["second"]["a"]["id"]
            d = match["second"]["b"]["id"]
            results.append({"id": a, "is_won": is_won})
            results.append({"id": b, "is_won": is_won})
            results.append({"id": c, "is_won": not is_won})
            results.append({"id": d, "is_won": not is_won})

            if a < b:
                partner = Partner.objects.get(a=a, b=b)
            else:
                partner = Partner.objects.get(a=b, b=a)

            partner.game_count += 1
            partner.save()

            if c < d:
                partner = Partner.objects.get(a=c, b=d)
            else:
                partner = Partner.objects.get(a=d, b=c)

            partner.game_count += 1
            partner.save()

        for result in results:
            player = Player.objects.get(pk=result["id"])
            player.played += 1
            player.won += 1 if result["is_won"] else 0
            player.lost += 1 if not result["is_won"] else 0

            player.save()
        return results

    def get(self, request):
        tournament_pk = request.GET.get('tournament')

        tournament = Tournament.objects.get(pk=tournament_pk)
        pairs = list(Partner.objects.all().order_by('game_count'))

        players_order = []

        for pair in pairs:
            if pair.a.pk not in players_order and pair.b.pk not in players_order:
                players_order.append(pair.a.pk)
                players_order.append(pair.b.pk)

        print("players_order", players_order)

        ordering = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(players_order)])

        players = list(Player.objects.filter(tournament=tournament_pk).order_by('played', ordering)[:tournament.ground_count * 4])

        players = players[:-(players.__len__() % 4)]

        print("not sorted", list(map(lambda x: x.pk, players)))

        players = sorted(players, key=lambda x: players_order.index(x.pk) if x.pk in players_order else len(players_order))
        print("playersplayersplayers", list(map(lambda x: x.pk, players)))

        players_dict = {player.pk: player for player in players}

        average_rank = statistics.mean([player.rank for player in players])
        print("average_rank", average_rank)

        players_pk = [player.pk for player in players]
        partners = Partner.objects.filter(a__in=players_pk, b__in=players_pk).order_by('game_count')

        for pair in partners:
            pair.rank = players_dict[pair.a.pk].rank + players_dict[pair.b.pk].rank

        sorted_pairs = sorted(partners, key=lambda e: (e.game_count, abs(average_rank * 2 - e.rank)))

        print("sorted_pairs", sorted_pairs)

        pairing = []

        for _ in range(round(players.__len__() / 2)):
            player_A = players.pop()
            pair = next(pair for pair in sorted_pairs if pair.a == player_A or pair.b == player_A)
            if pair.a == player_A:
                player_B = pair.b
            else:
                player_B = pair.a

            player_B_index = players.index(player_B)

            player_B = players.pop(player_B_index)
            pairing.append({"a": player_A, "b": player_B, "rank": player_A.rank + player_B.rank})
            sorted_pairs = list(filter(lambda p: (p.a != player_A and p.b != player_A) and (p.a != player_B and p.b != player_B), sorted_pairs))

        sorted_pairing = sorted(pairing, key=lambda p: (p["rank"]))

        matchs = []

        for index in range(0, sorted_pairing.__len__(), 2):
            matchs.append({'first': sorted_pairing[index], 'second': sorted_pairing[index + 1]})

        self.updateResults(json.loads(json.dumps(matchs, cls=ModelEncoder)))

        return JsonResponse(matchs, safe=False, encoder=ModelEncoder)

    def post(self, request):
        matchup = json.loads(request.body.decode("utf-8"))
        results = self.updateResults(matchup)

        return JsonResponse(results, safe=False)
