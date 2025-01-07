# leagues/models.py
from django.db import models
from clubs.models import FootballClub
from django.db.models import F, ExpressionWrapper, IntegerField

class League(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50,default=0)
    founded_year = models.IntegerField(default=0)
    clubs = models.ManyToManyField(FootballClub, through='ClubLeagueAssociation', related_name='leagues')
   
    
    def _str_(self):
        return self.name

class ClubLeagueAssociation(models.Model):
    club = models.ForeignKey(FootballClub, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    # Additional fields can be added here, like year_joined, etc.

    def _str_(self):
        return f"{self.club.name} in {self.league.name}"
    
class LeagueStanding(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    club = models.ForeignKey(FootballClub, on_delete=models.CASCADE)
    matches_played = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    goals_scored = models.PositiveIntegerField(default=0)
    goals_conceded = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)
    points_difference = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.club.name} in {self.league.name} - Points: {self.points}, Points Difference: {self.points_difference}"

    class Meta:
        unique_together = ('league', 'club')