from django.test import TestCase
from badminton.models import Player
from django.db.utils import IntegrityError


class PlayerTest(TestCase):

    def create_player(self, firstname="John", lastname="Doe", level=4, gender="M"):
        return Player.objects.create(firstname=firstname, lastname=lastname, level=level, gender=gender)

    def test_player_creation(self):
        p = self.create_player()
        self.assertTrue(isinstance(p, Player))

    def test_player_creation_firstname_mandatory(self):
        with self.assertRaises(IntegrityError):
            self.create_player(firstname=None)

    def test_player_creation_lastname_mandatory(self):
        with self.assertRaises(IntegrityError):
            self.create_player(lastname=None)

    def test_player_creation_level_mandatory(self):
        with self.assertRaises(IntegrityError):
            self.create_player(level=None)

    def test_player_creation_gender_mandatory(self):
        with self.assertRaises(IntegrityError):
            self.create_player(gender=None)
