from django.db import models


class Partner(models.Model):

    a = models.ForeignKey('badminton.Player', blank=True, on_delete=models.CASCADE, related_name='partner_a')
    b = models.ForeignKey('badminton.Player', blank=True, on_delete=models.CASCADE, related_name='partner_b')
    game_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.a.name} - {self.b.name} - {self.game_count}"

    class Meta:
        app_label = 'badminton'
        constraints = [
            models.UniqueConstraint(
                fields=['a', 'b'], name='unique_a_b'
            )
        ]
