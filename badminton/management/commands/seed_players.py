from django.core.management.base import BaseCommand
from badminton.models import Competitor, Tournament, Player
from django.db import transaction


class Command(BaseCommand):
    help = 'Seeds the database with initial competitors'

    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():
                tournament = Tournament.objects.create(name="t1", ground_count=2)

                players_data = [
                    {
                        'firstname': 'player 0',
                        'lastname': 'r',
                        'level': 2,
                        'gender': 'F'
                    },
                    {
                        'firstname': 'player 1',
                        'lastname': 'r',
                        'level': 4,
                        'gender': 'F'
                    },
                ]

                for player_data in players_data:
                    player, created = Player.objects.get_or_create(
                        firstname=player_data['firstname'],
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

                competitors_data = [
                    {
                        'firstname': 'competitor',
                        'lastname': 'r',
                        'tournament': tournament,
                        'level': 2,
                        'gender': 'F'
                    },
                    {
                        'firstname': 'competitor',
                        'lastname': 'r',
                        'tournament': tournament,
                        'level': 4,
                        'gender': 'F'
                    },
                    {
                        'firstname': 'competitor',
                        'lastname': 'r',
                        'tournament': tournament,
                        'level': 4,
                        'gender': 'F'
                    },
                    {
                        'firstname': 'competitor',
                        'lastname': 'r',
                        'tournament': tournament,
                        'level': 6,
                        'gender': 'F'
                    },
                    {
                        'firstname': 'competitor',
                        'lastname': 'r',
                        'tournament': tournament,
                        'level': 2,
                        'gender': 'M'
                    },
                    {
                        'firstname': 'competitor',
                        'lastname': 'r',
                        'tournament': tournament,
                        'level': 4,
                        'gender': 'M'
                    },
                    {
                        'firstname': 'competitor',
                        'lastname': 'r',
                        'tournament': tournament,
                        'level': 4,
                        'gender': 'M'
                    },
                    {
                        'firstname': 'competitor',
                        'lastname': 'r',
                        'tournament': tournament,
                        'level': 6,
                        'gender': 'M'
                    },
                    {
                        'firstname': 'competitor',
                        'lastname': 'r',
                        'tournament': tournament,
                        'level': 2,
                        'gender': 'M'
                    },
                    {
                        'firstname': 'competitor',
                        'lastname': 'r',
                        'tournament': tournament,
                        'level': 4,
                        'gender': 'M'
                    },
                    {
                        'firstname': 'competitor',
                        'lastname': 'r',
                        'tournament': tournament,
                        'level': 4,
                        'gender': 'M'
                    },
                ]

                for index, competitor_data in enumerate(competitors_data):
                    competitors_data[index]["firstname"] += f" {index}"

                for competitor_data in competitors_data:
                    competitor, created = Competitor.objects.get_or_create(
                        firstname=competitor_data["firstname"],
                        defaults=competitor_data
                    )

                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Successfully created competitor "{competitor.firstname}"')
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f'Competitor "{competitor.firstname}" already exists')
                        )

                players_data = [
                    {
                        'firstname': 'player z',
                        'lastname': 'r',
                        'level': 2,
                        'gender': 'F'
                    },
                    {
                        'firstname': 'player y',
                        'lastname': 'r',
                        'level': 4,
                        'gender': 'F'
                    },
                ]

                for player_data in players_data:
                    player, created = Player.objects.get_or_create(
                        firstname=player_data['firstname'],
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

                competitors_data = [
                    {
                        'firstname': 'competitor yy',
                        'lastname': 'r',
                        'tournament': tournament,
                        'level': 2,
                        'gender': 'F'
                    },
                    {
                        'firstname': 'competitor zz',
                        'lastname': 'r',
                        'tournament': tournament,
                        'level': 4,
                        'gender': 'F'
                    },
                ]

                for competitor_data in competitors_data:
                    competitor, created = Competitor.objects.get_or_create(
                        firstname=competitor_data["firstname"],
                        defaults=competitor_data
                    )

                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Successfully created competitor "{competitor.firstname}"')
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f'Competitor "{competitor.firstname}" already exists')
                        )
        except Exception as e:
            # If any error occurs, the transaction will be rolled back
            self.stdout.write(
                self.style.ERROR(f"Error occurred while seeding tournaments: {str(e)}")
            )
            raise e
