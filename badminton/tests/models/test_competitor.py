from django.test import TestCase
from badminton.models import Competitor, Partner
from django.db.utils import IntegrityError
from .test_player import PlayerTest
from .test_tournament import TournamentTest


class CompetitorTest(TestCase):

    tournamentTest = TournamentTest()
    playerTest = PlayerTest()

    def create_competitor(self, tournament, firstname="John", lastname="Doe", level=4, gender="M"):
        player = self.playerTest.create_player(firstname, lastname, level, gender)
        return Competitor.objects.create(player=player, tournament=tournament)

    def test_competitor_creation(self):
        t = self.tournamentTest.create_tournament()

        c = self.create_competitor(t)
        self.assertTrue(isinstance(c, Competitor))
        self.assertEqual(c.won, 0)
        self.assertEqual(c.lost, 0)
        self.assertEqual(c.played, 0)
        self.assertEqual(c.rank, 4)

    def test_competitor_creation_player_mandatory(self):
        t = self.tournamentTest.create_tournament()

        with self.assertRaises(IntegrityError):
            Competitor.objects.create(tournament=t)

    def test_competitor_creation_tournament_mandatory(self):
        p = self.playerTest.create_player()

        with self.assertRaises(IntegrityError):
            Competitor.objects.create(player=p)

    def test_competitor_creation_partner_update(self):
        """
        Regle d'implémentation : A chaque nouveau Competitor, on doit créer toutes les paires de Partner possible pour le tournoi choisi
        """
        t1 = self.tournamentTest.create_tournament()

        c1 = self.create_competitor(t1)
        self.assertEqual(Partner.objects.count(), 0)
        c2 = self.create_competitor(t1)
        self.assertEqual(Partner.objects.count(), 1)
        c3 = self.create_competitor(t1)
        self.assertEqual(Partner.objects.count(), 3)

        t2 = self.tournamentTest.create_tournament()
        self.create_competitor(t2)
        self.create_competitor(t2)

        partners = Partner.objects.filter(tournament=t1)
        expected_pairs = {(c1, c2), (c1, c3), (c2, c3)}
        actual_pairs = {(p.a, p.b) for p in partners}
        self.assertEqual(actual_pairs, expected_pairs)

        for partner in partners:
            self.assertEqual(partner.game_count, 0)

    def test_competitor_update_rank_update(self):
        """
        Regle métier : Le rank est calculé avec la formule suivante : level + ratio de matchs gagnés - ratio de matchs perdus
        Objectif : tenir compte de la performance du joueur durant le tournoi
        """
        t1 = self.tournamentTest.create_tournament()
        c1 = self.create_competitor(t1, level=4)
        c1.won = 1
        c1.save()
        self.assertEqual(c1.rank, 4 + 1)

        c1.played = 8
        c1.save()
        self.assertEqual(c1.rank, 4 + 1)

        c1.lost = 3
        c1.save()
        self.assertAlmostEqual(c1.rank, 4 + (1 / 4) - (3 / 4))

    def test_competitor_creation_set_played_to_max(self):
        """
        Regle métier : Lorsqu'un joueur intègre un tournoi en cours, il commence avec un nombre de match joué égal au maximum.
        Objectif : éviter de faire jouer ce nouveau joueur à tous les rounds (pour rattraper son retard de match joué)
        """
        t1 = self.tournamentTest.create_tournament()
        c1 = self.create_competitor(t1)
        c1.played = 4
        c1.save()
        c2 = self.create_competitor(t1)
        self.assertEqual(c2.played, 4)

    def test_competitor_is_playing_set_played_to_max(self):
        """
        Regle métier : Lorsqu'un joueur sort du tournoi et reviens, son nombre de match joué égal au maximum.
        Objectif : éviter de faire jouer ce joueur à tous les rounds (pour rattraper son retard de match joué)
        """
        t1 = self.tournamentTest.create_tournament()
        c1 = self.create_competitor(t1)
        c2 = self.create_competitor(t1)
        c2.is_playing = False
        c2.save()
        c1.played = 4
        c1.save()
        c2.is_playing = True
        c2.save()
        self.assertEqual(c2.played, 4)
