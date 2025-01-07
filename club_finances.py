import os
import django
from random import shuffle



# Setting up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dbproject.settings')
django.setup()

import random
from clubs.models import FootballClub
from transfer.models import ClubFinances

def assign_random_finances():
    for club in FootballClub.objects.all():
        random_funds = random.randint(30_000_000, 600_000_000)  # Generate integer values
        ClubFinances.objects.update_or_create(
            club=club,
            defaults={'available_funds': random_funds}
        )
        print(f"Set finances for {club.name}: €{random_funds}")

# Run this in the Django shell
assign_random_finances()
