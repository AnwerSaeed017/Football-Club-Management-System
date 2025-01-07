from django.db import models

# Create your models here.

class FootballClub(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ClubDetails(models.Model):
    club = models.OneToOneField('FootballClub', on_delete=models.CASCADE)
    stadium_name = models.CharField(max_length=100)
    stadium_capacity = models.PositiveIntegerField()
    stadium_location = models.CharField(max_length=200)
    stadium_opened_year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.club.name} Details"



