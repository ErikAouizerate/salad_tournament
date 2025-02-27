from django.core.management.base import BaseCommand
from badminton.models import Player, Tournament
from django.db import transaction


class Command(BaseCommand):
    help = 'Seeds the database with initial players'

    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():
                tournament = Tournament.objects.create(name="t1", ground_count=6)

                players_data = [
                    {
                        'name': 'player',
                        'tournament': tournament,
                        'level': 2
                    },
                    {
                        'name': 'player',
                        'tournament': tournament,
                        'level': 4
                    },
                    {
                        'name': 'player',
                        'tournament': tournament,
                        'level': 4
                    },
                    {
                        'name': 'player',
                        'tournament': tournament,
                        'level': 6
                    },
                    {
                        'name': 'player',
                        'tournament': tournament,
                        'level': 2
                    },
                    {
                        'name': 'player',
                        'tournament': tournament,
                        'level': 4
                    },
                    {
                        'name': 'player',
                        'tournament': tournament,
                        'level': 4
                    },
                    {
                        'name': 'player',
                        'tournament': tournament,
                        'level': 6
                    },
                    {
                        'name': 'player',
                        'tournament': tournament,
                        'level': 2
                    },
                    {
                        'name': 'player',
                        'tournament': tournament,
                        'level': 4
                    },
                    {
                        'name': 'player',
                        'tournament': tournament,
                        'level': 4
                    },
                ]

                for index, player_data in enumerate(players_data):
                    players_data[index]["name"] += f" {index}"

                for player_data in players_data:
                    player, created = Player.objects.get_or_create(
                        name=player_data["name"],
                        defaults=player_data
                    )

                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Successfully created player "{player.name}"')
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f'Player "{player.name}" already exists')
                        )
        except Exception as e:
            # If any error occurs, the transaction will be rolled back
            self.stdout.write(
                self.style.ERROR(f"Error occurred while seeding tournaments: {str(e)}")
            )
            raise e
