# Create your models here.
from django.db import models
from clubs.models import FootballClub
from leagues.models import League 

class MatchSchedule(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    home_team = models.ForeignKey(FootballClub, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(FootballClub, related_name='away_matches', on_delete=models.CASCADE)
    match_date = models.DateField()
    match_occurred = models.BooleanField(default=False)  # New field

    class Meta:
        unique_together = ('league', 'home_team', 'away_team', 'match_date')
        ordering = ['match_date']

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.match_date}"