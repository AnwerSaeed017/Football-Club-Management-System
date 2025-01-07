from django.db import models
from clubs.models import FootballClub
# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    nationality = models.CharField(max_length=50)
    position = models.CharField(max_length=30)
    club_name = models.CharField(max_length=100, blank=True, null=True)  # Name of the club
    image_url = models.URLField(max_length=200, blank=True, null=True)  # URL for the player's image

    def __str__(self):
        return self.name

class PlayerClubAssociation(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    club = models.ForeignKey(FootballClub, on_delete=models.CASCADE)
    market_value = models.DecimalField(max_digits=12, decimal_places=2,default=0)

    def __str__(self):
        return f"{self.player.name} at {self.club.name} (Market Value: {self.market_value})"
    
class PlayerAttribute(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE)
    speed = models.IntegerField()  # Scale of 1-100
    strength = models.IntegerField()
    stamina = models.IntegerField()
    agility = models.IntegerField()
    passing = models.IntegerField()
    dribbling = models.IntegerField()
    shooting = models.IntegerField()
    heading = models.IntegerField()
    tackling = models.IntegerField()
    positioning = models.IntegerField()
    vision = models.IntegerField()
    composure = models.IntegerField()
    crossing = models.IntegerField()
    finishing = models.IntegerField()
    freekicks = models.IntegerField()
    def __str__(self):
        return f"{self.player.name}'s Attributes"


#class PlayerStatistic(models.Model):
     #player = models.ForeignKey(Player, on_delete=models.CASCADE)
     #matches_played = models.IntegerField(default=0)
     #goals = models.IntegerField(default=0)
     #assists = models.IntegerField(default=0)
     #yellow_cards = models.IntegerField(default=0)
     #red_cards = models.IntegerField(default=0)

     #def __str__(self):
     #    return f"{self.player.name}'s Statistics"
