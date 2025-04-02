from django.db import models
from .player import Player
from .partner import Partner


class Competitor(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE)
    tournament = models.ForeignKey('badminton.Tournament', blank=True, on_delete=models.CASCADE)
    won = models.IntegerField(default=0)
    lost = models.IntegerField(default=0)
    played = models.IntegerField(default=0)
    rank = models.FloatField(default=0)
    is_playing = models.BooleanField(blank=False, null=False, default=True)

    def calculate_rank(self):
        if self.played == 0:
            return self.player.level
        won_ratio = self.won / self.played
        lost_ratio = self.lost / self.played
        return self.player.level + won_ratio - lost_ratio

    def __str__(self):
        if self.player:
            return f"({self.id}) {self.player.firstname} {self.player.lastname}, played: {self.played}"
        return f"({self.id}) Unknown Player, played: {self.played}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:
            competitors = list(Competitor.objects.filter(tournament=self.tournament))

        self.rank = self.calculate_rank()
        super().save(*args, **kwargs)

        if is_new:
            for competitor in competitors:
                if competitor.id < self.id:
                    partner = Partner.objects.create(a=competitor, b=self, tournament=self.tournament)
                else:
                    partner = Partner.objects.create(a=self, b=competitor, tournament=self.tournament)

                partner.save()

    class Meta:
        app_label = 'badminton'
