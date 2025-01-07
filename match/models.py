from django.db import models

# Create your models here.
from django.db import models
from schedule.models import MatchSchedule
from django.contrib.auth.models import User

class MatchResult(models.Model):
    match = models.ForeignKey(MatchSchedule, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)  # Add a reference to the User
    home_team_goals = models.PositiveIntegerField(default=0)
    away_team_goals = models.PositiveIntegerField(default=0)
    match_date = models.DateTimeField()

    def __str__(self):
        return f"Match {self.match.id}: {self.match.home_team} vs {self.match.away_team} - {self.match_date}"