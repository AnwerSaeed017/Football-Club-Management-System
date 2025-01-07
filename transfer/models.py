from django.db import models
from clubs.models import FootballClub
from players.models import Player
# Create your models here.

class ClubFinances(models.Model):
    club = models.OneToOneField(FootballClub, on_delete=models.CASCADE, related_name='finances')
    available_funds = models.BigIntegerField()  # Changed from DecimalField to BigIntegerField

    def __str__(self):
        return f"{self.club.name} - Funds: €{self.available_funds}"

class PlayerTransfer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    from_club = models.ForeignKey(FootballClub, related_name='transfers_out', on_delete=models.CASCADE)
    to_club = models.ForeignKey(FootballClub, related_name='transfers_in', on_delete=models.CASCADE)
    transfer_date = models.DateField(auto_now_add=True)
    transfer_fee = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Transfer of {self.player.name} from {self.from_club.name} to {self.to_club.name}"
