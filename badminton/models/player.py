from django.db import models


class Player(models.Model):
    class Level(models.IntegerChoices):
        NOVICE = 2
        MIDDLE = 4
        STRONG = 6

    class Gender(models.TextChoices):
        MALE = "M"
        FEMALE = "F"

    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    level = models.IntegerField(Level.choices, default=Level.NOVICE)
    gender = models.CharField(Gender.choices, max_length=1, default=Gender.MALE)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    class Meta:
        app_label = 'badminton'
