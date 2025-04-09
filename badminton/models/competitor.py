from django.db import models, IntegrityError
from .player import Player
from .partner import Partner
from .tournament import Tournament
from django.db.models import Max


class Competitor(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    won = models.IntegerField(default=0)
    lost = models.IntegerField(default=0)
    played = models.IntegerField(default=0)
    rank = models.FloatField(default=0)
    is_playing = models.BooleanField(default=True)

    def __calculate_rank(self):
        real_played_match = self.won + self.lost
        if real_played_match == 0:
            return self.player.level
        won_ratio = self.won / real_played_match
        lost_ratio = self.lost / real_played_match
        return self.player.level + won_ratio - lost_ratio

    def __str__(self):
        if self.player:
            return f"({self.id}) {self.player.firstname} {self.player.lastname}, played: {self.played}"
        return f"({self.id}) Unknown Player, played: {self.played}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if not self.tournament_id:
            raise IntegrityError("Tournament must be set for a Competitor.")

        if not self.player_id:
            raise IntegrityError("Player must be set for a Competitor.")

        if is_new:
            competitors = list(Competitor.objects.filter(tournament=self.tournament))
            self.played = self.__get_max_played()
        else:
            old_instance = Competitor.objects.get(pk=self.pk)
            if not old_instance.is_playing and self.is_playing:
                max_played = self.__get_max_played()
                if self.played < max_played:
                    self.played = max_played

        self.rank = self.__calculate_rank()
        super().save(*args, **kwargs)

        if is_new:
            for competitor in competitors:
                if competitor.id < self.id:
                    partner = Partner.objects.create(a=competitor, b=self, tournament=self.tournament)
                else:
                    partner = Partner.objects.create(a=self, b=competitor, tournament=self.tournament)

                partner.save()

    def __get_max_played(self):
        max_played = Competitor.objects.filter(tournament=self.tournament, is_playing=True).aggregate(Max('played'))['played__max']
        return max_played or 0

    class Meta:
        app_label = 'badminton'
        constraints = [
            models.UniqueConstraint(
                fields=['player', 'tournament'], name='unique_competitor_per_tournament'
            )
        ]
