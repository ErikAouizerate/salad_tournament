from django.core.management.base import BaseCommand
from badminton.models import Tournament, User


class Command(BaseCommand):
    help = 'Seeds the database with initial players'

    def handle(self, *args, **kwargs):
        # tournament = Tournament.objects.create(name="t1")

        User.objects.all().delete()
        Tournament.objects.all().delete()
