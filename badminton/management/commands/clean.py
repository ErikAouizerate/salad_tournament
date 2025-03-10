from django.core.management.base import BaseCommand
from badminton.models import Tournament, Player


class Command(BaseCommand):
    help = 'Seeds the database with initial players'

    def handle(self, *args, **kwargs):
        # tournament = Tournament.objects.create(name="t1")

        Player.objects.all().delete()
        Tournament.objects.all().delete()
