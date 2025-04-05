from badminton.models import Competitor, Partner
import statistics
import random
import math
from django.db.models import Window, Max
from django.db.models.functions import RowNumber, Random


class TournamentService:

    def __init__(self, tournament):
        self.tournament = tournament

    def updateResults(self, matchs, toFinish):
        results = []
        for match in matchs:
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
                partner = Partner.objects.get(a=a, b=b, tournament=self.tournament.id)
            else:
                partner = Partner.objects.get(a=b, b=a, tournament=self.tournament.id)

            partner.game_count += 1
            partner.save()

            if c < d:
                partner = Partner.objects.get(a=c, b=d, tournament=self.tournament.id)
            else:
                partner = Partner.objects.get(a=d, b=c, tournament=self.tournament.id)

            partner.game_count += 1
            partner.save()

        max_played = Competitor.objects.filter(tournament=self.tournament, is_playing=True).aggregate(Max('played'))['played__max']

        for result in results:
            competitor = Competitor.objects.get(pk=result["id"])
            if not toFinish or competitor.played < max_played:
                competitor.played += 1
                competitor.won += 1 if result["has_won"] else 0
                competitor.lost += 1 if not result["has_won"] else 0

                competitor.save()
        return results

    def __get_competitors_short_list(self):
        competitors = list(
            Competitor.objects.filter(tournament=self.tournament)
            .filter(is_playing=True)
            .annotate(
                random_group=Window(
                    expression=RowNumber(),
                    order_by=Random()
                )
            )
            .order_by('played', 'random_group')
            [:self.tournament.ground_count * 4]
        )

        if competitors.__len__() % 4 != 0:
            competitors = competitors[:-(competitors.__len__() % 4)]

        return competitors

    def __get_bench(self, competitors):
        players_pk = [competitor.pk for competitor in competitors]

        return list(Competitor.objects.filter(tournament=self.tournament).exclude(pk__in=players_pk))

    def __get_partners(self, competitors):

        players_dict = {competitor.pk: competitor for competitor in competitors}

        players_pk = [competitor.pk for competitor in competitors]
        partners = Partner.objects.filter(a__in=players_pk, b__in=players_pk).order_by('game_count')

        for partner in partners:
            partner.rank = players_dict[partner.a.pk].rank + players_dict[partner.b.pk].rank

        return partners

    def __get_pairings(self, _competitors, _partners):
        competitors = list(_competitors)
        partners = list(_partners)

        average_rank = statistics.mean([competitor.rank for competitor in competitors])
        partners = sorted(partners, key=lambda e: (e.game_count, abs(average_rank * 2 - e.rank)))

        pairings = []

        for _ in range(round(competitors.__len__() / 2)):
            player_A = competitors.pop()
            pair = next(pair for pair in partners if pair.a == player_A or pair.b == player_A)
            if pair.a == player_A:
                player_B = pair.b
            else:
                player_B = pair.a

            player_B_index = competitors.index(player_B)

            player_B = competitors.pop(player_B_index)
            pairings.append({"a": player_A, "b": player_B, "rank": player_A.rank + player_B.rank})
            partners = list(filter(lambda p: (p.a != player_A and p.b != player_A) and (p.a != player_B and p.b != player_B), partners))

        return pairings

    def __get_matchs(self, competitors):

        partners = self.__get_partners(competitors)

        pairings = self.__get_pairings(competitors, partners)

        pairings = sorted(pairings, key=lambda p: (p["rank"]))

        matchs = []

        for index in range(0, pairings.__len__(), 2):
            matchs.append({'teamA': pairings[index], 'teamB': pairings[index + 1],
                           'rankDelta': pairings[index]["rank"] - pairings[index + 1]["rank"]})
        return matchs

    def pairing(self):

        competitors = self.__get_competitors_short_list()

        bench = self.__get_bench(competitors)

        if len(competitors) == 0:
            matchs = []
            missing_rounds = math.inf
        else:
            matchs = self.__get_matchs(competitors)
            missing_rounds = self.__get_missing_next_rounds(matchs)

        return {"pairings": matchs, "bench": bench, "missing_rounds_after_this_one": missing_rounds}

    def __get_missing_next_rounds(self, pairings):
        pairings_ids = []
        for pairing in pairings:
            pairings_ids.append(pairing["teamA"]['a'].id)
            pairings_ids.append(pairing["teamA"]['b'].id)
            pairings_ids.append(pairing["teamB"]['a'].id)
            pairings_ids.append(pairing["teamB"]['b'].id)

        all_competitors = list(Competitor.objects.filter(tournament=self.tournament).filter(is_playing=True))
        max_played_games = 0
        for competitor in all_competitors:
            if competitor.id in pairings_ids:
                competitor.played += 1
            if competitor.played > max_played_games:
                max_played_games = competitor.played

        return self.__missing_rounds(all_competitors, max_played_games)

    def get_missing_rounds(self):
        max_played = Competitor.objects.filter(tournament=self.tournament, is_playing=True).aggregate(Max('played'))['played__max']
        all_competitors = list(Competitor.objects.filter(tournament=self.tournament).filter(is_playing=True))
        return self.__missing_rounds(all_competitors, max_played)

    def __missing_rounds(self, all_competitors, max_played):
        competitors_need_play = 0
        for competitor in all_competitors:
            if competitor.played < max_played:
                competitors_need_play += 1

        return math.ceil(competitors_need_play / (self.tournament.ground_count * 4))

    def play_random_games(self, matchup, toFinish):
        for match in matchup['pairings']:
            match['hasTeamAWon'] = bool(random.getrandbits(1))

        self.updateResults(matchup['pairings'], toFinish)
