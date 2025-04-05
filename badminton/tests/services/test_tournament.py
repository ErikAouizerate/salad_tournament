from django.test import TestCase
from badminton.tests.models.test_tournament import TournamentTest
from badminton.tests.models.test_competitor import CompetitorTest
from badminton.services.tournament_service import TournamentService
from badminton.models.competitor import Competitor
from badminton.models.partner import Partner


class TournamentServiceTest(TestCase):

    def setUp(self):
        self.tournamentTest = TournamentTest()
        self.competitorTest = CompetitorTest()

    def create_tournament(self):
        t1 = self.tournamentTest.create_tournament(ground_count=1)
        c1 = self.competitorTest.create_competitor(t1, level=2)
        c2 = self.competitorTest.create_competitor(t1, level=4)
        c3 = self.competitorTest.create_competitor(t1, level=4)
        c4 = self.competitorTest.create_competitor(t1, level=6)
        self.tournamentService = TournamentService(t1)

        return {"t": t1, "cs": (c1, c2, c3, c4)}

    def test_update_results(self):
        """
        Règle métier : le nombre de match joué, gagné et perdu est mis à jour
        """
        base_tournament = self.create_tournament()
        results = [{
            "teamA": [{"id": base_tournament["cs"][0].id}, {"id": base_tournament["cs"][1].id}],
            "teamB": [{"id": base_tournament["cs"][2].id}, {"id": base_tournament["cs"][3].id}],
            "hasTeamAWon": True
        }]
        self.tournamentService.updateResults(results, False)
        c1, c2, c3, c4 = base_tournament["cs"]

        c1.refresh_from_db()
        c2.refresh_from_db()
        c3.refresh_from_db()
        c4.refresh_from_db()

        self.assertEqual(c1.played, 1)
        self.assertEqual(c2.played, 1)
        self.assertEqual(c3.played, 1)
        self.assertEqual(c4.played, 1)

        self.assertEqual(c1.won, 1)
        self.assertEqual(c2.won, 1)
        self.assertEqual(c3.won, 0)
        self.assertEqual(c4.won, 0)

        self.assertEqual(c1.lost, 0)
        self.assertEqual(c2.lost, 0)
        self.assertEqual(c3.lost, 1)
        self.assertEqual(c4.lost, 1)

    def test_update_results_partner(self):
        """
        Règle d'implémentation : Chaque pair de joueur est incrémenté par le nombre de match joué ensemble
        """
        base_tournament = self.create_tournament()
        results = [{
            "teamA": [{"id": base_tournament["cs"][0].id}, {"id": base_tournament["cs"][1].id}],
            "teamB": [{"id": base_tournament["cs"][2].id}, {"id": base_tournament["cs"][3].id}],
            "hasTeamAWon": True
        }]
        self.tournamentService.updateResults(results, False)
        self.assertEqual(Partner.objects.exclude(game_count=0).count(), 2)
        self.assertEqual(Partner.objects.get(a=base_tournament["cs"][0], b=base_tournament["cs"][1]).game_count, 1)
        self.assertEqual(Partner.objects.get(a=base_tournament["cs"][2], b=base_tournament["cs"][3]).game_count, 1)

    def test_update_results_switch(self):
        """
        Règle métier : l'ordre des Competitors dans les resultats n'a pas d'importance
        """
        base_tournament = self.create_tournament()
        results = [{
            "teamA": [{"id": base_tournament["cs"][1].id}, {"id": base_tournament["cs"][0].id}],
            "teamB": [{"id": base_tournament["cs"][3].id}, {"id": base_tournament["cs"][2].id}],
            "hasTeamAWon": True
        }]
        self.tournamentService.updateResults(results, False)

        self.assertEqual(Partner.objects.exclude(game_count=0).count(), 2)
        self.assertEqual(Partner.objects.get(a=base_tournament["cs"][0], b=base_tournament["cs"][1]).game_count, 1)
        self.assertEqual(Partner.objects.get(a=base_tournament["cs"][2], b=base_tournament["cs"][3]).game_count, 1)

    def test_update_results_to_finish(self):
        """
        Règle métier : Pour finir un tournoi, tous les competitors doivent avoir fait le même nombre match
        On ne comptabilise pas les matchs des competitors ayant déjà fait le nombre maximal de match
        """
        base_tournament = self.create_tournament()
        results = [{
            "teamA": [{"id": base_tournament["cs"][0].id}, {"id": base_tournament["cs"][1].id}],
            "teamB": [{"id": base_tournament["cs"][2].id}, {"id": base_tournament["cs"][3].id}],
            "hasTeamAWon": True
        }]
        c1, c2, c3, c4 = base_tournament["cs"]
        c1.played = 3
        c1.save()
        self.tournamentService.updateResults(results, True)

        c1.refresh_from_db()
        c2.refresh_from_db()
        c3.refresh_from_db()
        c4.refresh_from_db()

        self.assertEqual(c1.played, 3)
        self.assertEqual(c2.played, 1)
        self.assertEqual(c3.played, 1)
        self.assertEqual(c4.played, 1)

    def test_pairing_less_played_first(self):
        """
        Règle métier : On doit faire jouer en priorité les Competitors ayant le moins de match joué
        """
        base_tournament = self.create_tournament()
        self.competitorTest.create_competitor(base_tournament["t"], level=2)
        c1 = base_tournament["cs"][0]
        c1.played = 1
        c1.save()
        pairing_1 = self.tournamentService.pairing()
        self.assertEqual(len(pairing_1["pairings"]), 1)
        self.assertNotEqual(pairing_1["pairings"][0]["teamA"]["a"], c1)
        self.assertNotEqual(pairing_1["pairings"][0]["teamA"]["b"], c1)
        self.assertNotEqual(pairing_1["pairings"][0]["teamB"]["a"], c1)
        self.assertNotEqual(pairing_1["pairings"][0]["teamB"]["b"], c1)

    def test_pairing_ground(self):
        """
        Règle métier : On doit maximiser l'utilisation des terrains disponible
        """
        base_tournament = self.create_tournament()
        for _ in range(5):
            self.competitorTest.create_competitor(base_tournament["t"], level=2)
        base_tournament["t"].ground_count = 3
        base_tournament["t"].save()

        pairing_1 = self.tournamentService.pairing()
        self.assertEqual(len(pairing_1["pairings"]), 2)

    def test_pairing_full_ground(self):
        """
        Règle métier : On doit faire uniquement des matchs avec 4 competitors tous différents par terrain
        """
        base_tournament = self.create_tournament()
        for _ in range(6):
            self.competitorTest.create_competitor(base_tournament["t"], level=2)
        base_tournament["t"].ground_count = 3
        base_tournament["t"].save()

        pairing_1 = self.tournamentService.pairing()
        self.assertEqual(len(pairing_1["pairings"]), 2)
        competitors = []
        for pairing in pairing_1["pairings"]:
            self.assertIsInstance(pairing["teamA"]["a"], Competitor)
            self.assertIsInstance(pairing["teamA"]["b"], Competitor)
            self.assertIsInstance(pairing["teamB"]["a"], Competitor)
            self.assertIsInstance(pairing["teamB"]["b"], Competitor)
            competitors.append(pairing["teamA"]["a"])
            competitors.append(pairing["teamA"]["b"])
            competitors.append(pairing["teamB"]["a"])
            competitors.append(pairing["teamB"]["b"])

        self.assertEqual(len(competitors), len(set(competitors)))

    def test_pairing_bench(self):
        """
        Règle métier : On doit obtenir la liste des competitors qui ne joue pas à ce round
        """
        base_tournament = self.create_tournament()
        self.competitorTest.create_competitor(base_tournament["t"], level=2)
        c1 = base_tournament["cs"][0]
        c1.played = 1
        c1.save()
        pairing_1 = self.tournamentService.pairing()
        self.assertEqual(len(pairing_1["bench"]), 1)

    def test_pairing_balanced(self):
        """
        Règle métier : On doit proposer des match équilibré
        """
        self.create_tournament()
        pairing_1 = self.tournamentService.pairing()
        self.assertEqual(pairing_1["pairings"][0]["teamA"]["rank"], 8)
        self.assertEqual(pairing_1["pairings"][0]["teamB"]["rank"], 8)

    def test_pairing_new_partners(self):
        """
        Règle métier : On doit favoriser des équipes de Competitors qui n'ont pas encore joué ensemble
        """
        base_tournament = self.create_tournament()
        c1, c2, c3, c4 = base_tournament["cs"]
        pair_1 = Partner.objects.get(a=c1, b=c4)
        pair_1.game_count = 1
        pair_1.save()

        pair_2 = Partner.objects.get(a=c2, b=c3)
        pair_2.game_count = 1
        pair_2.save()

        pairing_1 = self.tournamentService.pairing()
        pair_already_played_1 = set((c1, c4))
        pair_already_played_2 = set((c2, c3))

        new_pair_1 = set((pairing_1["pairings"][0]["teamA"]["a"], pairing_1["pairings"][0]["teamA"]["b"]))
        new_pair_2 = set((pairing_1["pairings"][0]["teamB"]["a"], pairing_1["pairings"][0]["teamB"]["b"]))

        self.assertNotEqual(new_pair_1, pair_already_played_1)
        self.assertNotEqual(new_pair_1, pair_already_played_2)
        self.assertNotEqual(new_pair_2, pair_already_played_1)
        self.assertNotEqual(new_pair_2, pair_already_played_2)

    def test_pairing_missing_rounds(self):
        """
        Règle métier : On doit renvoyer le nombre minimum de round pour finir le tournoi
        """
        base_tournament = self.create_tournament()
        pairing_1 = self.tournamentService.pairing()
        self.assertEqual(pairing_1["missing_rounds_after_this_one"], 0)
        self.competitorTest.create_competitor(base_tournament["t"], level=2)
        pairing_1 = self.tournamentService.pairing()
        self.assertEqual(pairing_1["missing_rounds_after_this_one"], 1)
