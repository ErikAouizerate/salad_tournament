from django.core.management.base import BaseCommand
from badminton.models import Player, Tournament
from django.db import transaction


class Command(BaseCommand):
    help = 'Seeds the database with initial players'

    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():
                tournament = Tournament.objects.create(name="t1", ground_count=2)

                players_data = [
                    {
                        'firstname': 'player',
                        'lastname': 'r',
                        'tournament': tournament,
                        'level': 2,
                        'gender': 'F'
                    },
                    {
                        'firstname': 'player',
                        'lastname': 'r',
                        'tournament': tournament,
                        'level': 4,
                        'gender': 'F'
                    },
                    {
                        'firstname': 'player',
                        'lastname': 'r',
                        'tournament': tournament,
                        'level': 4,
                        'gender': 'F'
                    },
                    {
                        'firstname': 'player',
                        'lastname': 'r',
                        'tournament': tournament,
                        'level': 6,
                        'gender': 'F'
                    },
                    {
                        'firstname': 'player',
                        'lastname': 'r',
                        'tournament': tournament,
                        'level': 2,
                        'gender': 'M'
                    },
                    {
                        'firstname': 'player',
                        'lastname': 'r',
                        'tournament': tournament,
                        'level': 4,
                        'gender': 'M'
                    },
                    {
                        'firstname': 'player',
                        'lastname': 'r',
                        'tournament': tournament,
                        'level': 4,
                        'gender': 'M'
                    },
                    {
                        'firstname': 'player',
                        'lastname': 'r',
                        'tournament': tournament,
                        'level': 6,
                        'gender': 'M'
                    },
                    {
                        'firstname': 'player',
                        'lastname': 'r',
                        'tournament': tournament,
                        'level': 2,
                        'gender': 'M'
                    },
                    {
                        'firstname': 'player',
                        'lastname': 'r',
                        'tournament': tournament,
                        'level': 4,
                        'gender': 'M'
                    },
                    {
                        'firstname': 'player',
                        'lastname': 'r',
                        'tournament': tournament,
                        'level': 4,
                        'gender': 'M'
                    },
                ]

                for index, player_data in enumerate(players_data):
                    players_data[index]["firstname"] += f" {index}"

                for player_data in players_data:
                    player, created = Player.objects.get_or_create(
                        firstname=player_data["firstname"],
                        defaults=player_data
                    )

                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Successfully created player "{player.firstname}"')
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f'Player "{player.firstname}" already exists')
                        )
        except Exception as e:
            # If any error occurs, the transaction will be rolled back
            self.stdout.write(
                self.style.ERROR(f"Error occurred while seeding tournaments: {str(e)}")
            )
            raise e
