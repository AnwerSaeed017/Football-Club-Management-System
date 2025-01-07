import os
import django
import datetime
from itertools import combinations
from random import shuffle
from django.db import transaction


# Setting up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dbproject.settings')
django.setup()

# Import your models here
from leagues.models import League
from clubs.models import FootballClub
from schedule.models import MatchSchedule

def create_match_schedule(teams, start_date, end_date):
    all_matches = list(combinations(teams, 2))
    shuffle(all_matches)

    match_dates = {}
    daily_matches = {}
    last_played = {team: start_date - datetime.timedelta(days=4) for team in teams}

    for match in all_matches:
        current_date = start_date
        while current_date <= end_date:
            if (current_date not in daily_matches or len(daily_matches[current_date]) < 3) and all(
                last_played[team] <= current_date - datetime.timedelta(days=3) for team in match
            ):
                daily_matches.setdefault(current_date, []).append(match)
                for team in match:
                    last_played[team] = current_date
                break
            current_date += datetime.timedelta(days=1)

    return daily_matches

def list_clubs_in_league(league_name):
    try:
        league = League.objects.get(name=league_name)
    except League.DoesNotExist:
        print(f"League '{league_name}' not found.")
        return

    clubs = list(league.clubs.all())
    print(f"Clubs in {league_name}:")
    for club in clubs:
        print(club.name)  # Assuming your FootballClub model has a 'name' field

    return clubs

def schedule_matches_for_league(league_name):
    try:
        league = League.objects.get(name=league_name)  # Fetch the League instance
    except League.DoesNotExist:
        print(f"League '{league_name}' not found.")
        return

    clubs = list_clubs_in_league(league_name)
    if not clubs:
        return

    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.date(2023, 6, 30)
    schedule = create_match_schedule(clubs, start_date, end_date)

    with transaction.atomic():  # Use atomic transactions to ensure data integrity
        for date, matches in sorted(schedule.items()):
            for home_team, away_team in matches:
                match_schedule_entry = MatchSchedule.objects.create(
                    league=league,  # Ensure this is a League instance
                    home_team=home_team,
                    away_team=away_team,
                    match_date=date
                )
                print(f"Match ID: {match_schedule_entry.id}, Date: {date}, Home Team: {home_team.name}, Away Team: {away_team.name}")

# Example usage
if __name__ == "__main__":
    league_name = "Premier League"  # Replace with your league name
    schedule_matches_for_league(league_name)
    
if __name__ == "__main__":
    league_name = "LaLiga"  # Change to LaLiga
    schedule_matches_for_league(league_name)
    
if __name__ == "__main__":
    league_name = "Bundesliga"  
    schedule_matches_for_league(league_name)
    
if __name__ == "__main__":
    league_name = "Serie A" 
    schedule_matches_for_league(league_name)
    
if __name__ == "__main__":
    league_name = "Ligue 1"  # Change to LaLiga
    schedule_matches_for_league(league_name)