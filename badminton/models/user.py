from django.db import models


class User(models.Model):
    class Level(models.IntegerChoices):
        NOVICE = 2
        MIDDLE = 4
        STRONG = 6

    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    level = models.IntegerField(Level.choices, default=Level.NOVICE)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    class Meta:
        app_label = 'badminton'
