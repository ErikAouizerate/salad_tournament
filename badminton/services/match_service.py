from badminton.models import Competitor, Tournament, Partner
from badminton.serializers import PairingsListSerializer, CompetitorSerializer
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
            competitor = Competitor.objects.get(pk=result["id"])
            competitor.played += 1
            competitor.won += 1 if result["has_won"] else 0
            competitor.lost += 1 if not result["has_won"] else 0

            competitor.save()
        return results

    @staticmethod
    def pairing(tounrnament_id):
        tournament = Tournament.objects.get(pk=tounrnament_id)

        # players_order = []

        competitors = list(Competitor.objects.filter(tournament=tounrnament_id).filter(is_playing=True).order_by('played')[:tournament.ground_count * 4])

        if competitors.__len__() % 4 != 0:
            competitors = competitors[:-(competitors.__len__() % 4)]

        players_pk = list(map(lambda x: x.pk, competitors))

        bench = list(Competitor.objects.exclude(pk__in=players_pk))

        # print("not sorted", list(map(lambda x: x.pk, competitors)))

        # competitors = sorted(competitors, key=lambda x: players_order.index(x.pk) if x.pk in players_order else len(players_order))
        # print("playersplayersplayers", list(map(lambda x: x.pk, competitors)))

        players_dict = {competitor.pk: competitor for competitor in competitors}

        average_rank = statistics.mean([competitor.rank for competitor in competitors])
        # print("average_rank", average_rank)

        players_pk = [competitor.pk for competitor in competitors]
        partners = Partner.objects.filter(a__in=players_pk, b__in=players_pk).order_by('game_count')

        for pair in partners:
            pair.rank = players_dict[pair.a.pk].rank + players_dict[pair.b.pk].rank

        sorted_pairs = sorted(partners, key=lambda e: (e.game_count, abs(average_rank * 2 - e.rank)))

        # print("sorted_pairs", sorted_pairs)

        pairing = []

        for _ in range(round(competitors.__len__() / 2)):
            player_A = competitors.pop()
            pair = next(pair for pair in sorted_pairs if pair.a == player_A or pair.b == player_A)
            if pair.a == player_A:
                player_B = pair.b
            else:
                player_B = pair.a

            player_B_index = competitors.index(player_B)

            player_B = competitors.pop(player_B_index)
            pairing.append({"a": player_A, "b": player_B, "rank": player_A.rank + player_B.rank})
            sorted_pairs = list(filter(lambda p: (p.a != player_A and p.b != player_A) and (p.a != player_B and p.b != player_B), sorted_pairs))

        sorted_pairing = sorted(pairing, key=lambda p: (p["rank"]))

        pairings = []

        for index in range(0, sorted_pairing.__len__(), 2):
            pairings.append({'teamA': sorted_pairing[index], 'teamB': sorted_pairing[index + 1]})

        # self.updateResults(json.loads(json.dumps(pairings, cls=ModelEncoder)))

        pairingsSerialized = PairingsListSerializer(pairings, many=True)
        benchSerialized = CompetitorSerializer(bench, many=True)

        return {"pairings": pairingsSerialized.data, "bench": benchSerialized.data}

    @staticmethod
    def play_games(matchup, tournament_id):
        for match in matchup['pairings']:
            match['hasTeamAWon'] = bool(random.getrandbits(1))
        matchup['tournamentId'] = tournament_id
        matchup['results'] = matchup['pairings']

        MatchService.updateResults(matchup)
