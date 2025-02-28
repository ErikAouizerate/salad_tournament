from badminton.models import Player, Tournament, Partner
from badminton.serializers import PairingsListSerializer, PlayerSerializer
import statistics
import random


class MatchService:
    @staticmethod
    def updateResults(body):
        tournament_id = body['tournamentId']
        results = []
        for match in body['results']:
            has_team_a_won = match['hasTeamAWon']
            a = match["teamA"][0]["id"]
            b = match["teamA"][1]["id"]
            c = match["teamB"][0]["id"]
            d = match["teamB"][1]["id"]
            results.append({"id": a, "has_won": has_team_a_won})
            results.append({"id": b, "has_won": has_team_a_won})
            results.append({"id": c, "has_won": not has_team_a_won})
            results.append({"id": d, "has_won": not has_team_a_won})

            if a < b:
                partner = Partner.objects.get(a=a, b=b, tournament=tournament_id)
            else:
                partner = Partner.objects.get(a=b, b=a, tournament=tournament_id)

            partner.game_count += 1
            partner.save()

            if c < d:
                partner = Partner.objects.get(a=c, b=d, tournament=tournament_id)
            else:
                partner = Partner.objects.get(a=d, b=c, tournament=tournament_id)

            partner.game_count += 1
            partner.save()

        for result in results:
            player = Player.objects.get(pk=result["id"])
            player.played += 1
            player.won += 1 if result["has_won"] else 0
            player.lost += 1 if not result["has_won"] else 0

            player.save()
        return results

    @staticmethod
    def pairing(tounrnament_id):
        tournament = Tournament.objects.get(pk=tounrnament_id)

        # players_order = []

        players = list(Player.objects.filter(tournament=tounrnament_id).order_by('played')[:tournament.ground_count * 4])

        if players.__len__() % 4 != 0:
            players = players[:-(players.__len__() % 4)]

        players_pk = list(map(lambda x: x.pk, players))

        bench = list(Player.objects.exclude(pk__in=players_pk))

        print("not sorted", list(map(lambda x: x.pk, players)))

        # players = sorted(players, key=lambda x: players_order.index(x.pk) if x.pk in players_order else len(players_order))
        # print("playersplayersplayers", list(map(lambda x: x.pk, players)))

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

        pairings = []

        for index in range(0, sorted_pairing.__len__(), 2):
            pairings.append({'teamA': sorted_pairing[index], 'teamB': sorted_pairing[index + 1]})

        # self.updateResults(json.loads(json.dumps(pairings, cls=ModelEncoder)))

        pairingsSerialized = PairingsListSerializer(pairings, many=True)
        benchSerialized = PlayerSerializer(bench, many=True)

        return {"pairings": pairingsSerialized.data, "bench": benchSerialized.data}

    @staticmethod
    def play_games(matchup, tournament_id):
        for match in matchup['pairings']:
            match['hasTeamAWon'] = bool(random.getrandbits(1))
        matchup['tournamentId'] = tournament_id
        matchup['results'] = matchup['pairings']
        print("matchup", matchup)

        MatchService.updateResults(matchup)
