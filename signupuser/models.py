from django.db import models
from django.contrib.auth.models import User  # Assuming you are using Django's built-in User model
from leagues.models import League
from clubs.models import FootballClub
from django.utils import timezone

class UserLeagueClubSelection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    club = models.ForeignKey(FootballClub, on_delete=models.CASCADE)
    selection_date = models.DateTimeField(default=timezone.now)  # Add a date attribute

    def __str__(self):
        return f"{self.user.username}'s Selection: League - {self.league.name}, Club - {self.club.name}"



