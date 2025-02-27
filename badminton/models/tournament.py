from django.db import models


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    ground_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'badminton'
