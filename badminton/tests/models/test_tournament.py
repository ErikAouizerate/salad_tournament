from django.test import TestCase
from badminton.models import Tournament
from django.db.utils import IntegrityError


class TournamentTest(TestCase):

    def create_tournament(self, name="t1"):
        return Tournament.objects.create(name=name)

    def test_tournament_creation(self):
        t = self.create_tournament()
        self.assertTrue(isinstance(t, Tournament))
        self.assertEqual(t.ground_count, 0)

    def test_tournament_creation_name_mandatory(self):
        with self.assertRaises(IntegrityError):
            self.create_tournament(name=None)
