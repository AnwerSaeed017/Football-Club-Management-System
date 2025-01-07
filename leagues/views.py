from django.shortcuts import render, redirect
from .models import League
from .models import LeagueStanding
import logging

def league_selection(request):
    if request.method == 'POST':
        selected_league_id = request.POST.get('league')
        request.session['selected_league_id'] = selected_league_id
        return redirect('club_selection')  # Redirect to club selection page

    leagues = League.objects.all()
    return render(request, 'leagues/league_selection.html', {'leagues': leagues})

def league_standings_view(request):
    # Retrieve the league standings queryset with calculated fields
    selected_league_id = request.session.get('selected_league_id')

    if selected_league_id is None:
        # Handle the case where no league is selected
        logging.warning("No league selected for viewing standings.")
        return redirect('league_selection') 
    standings = LeagueStanding.objects.filter(league_id=selected_league_id)
    
    # Sort the queryset using Python's sorted function
    standings = sorted(standings, key=lambda x: (-x.points, -x.points_difference, -x.goals_scored))

    # Render the data using a template (optional)
    context = {'standings': standings}
    return render(request, 'leagues/league_standing.html', context)

from clubs.models import FootballClub

def insert_clubs_into_leaguestanding(league_id):
    

    try:
        # Retrieve the league object with the specific ID
        league = League.objects.get(id=league_id)  # Replace '1' with the desired league ID
         # Get all the football clubs that belong to the specified league
        clubs = FootballClub.objects.filter(leagues=league)
    except League.DoesNotExist:
        # Handle the case where the league doesn't exist
        # You can log an error message or take appropriate action
        # For example, you can log an error message or take appropriate action
        logging.error(f"League with ID {league_id} does not exist.")

    # Iterate through each club and insert it into the leaguestanding table
    for club in clubs:
        # Check if a league standing record already exists for this club
        existing_record = LeagueStanding.objects.filter(club=club, league=league).exists()

        if not existing_record and league:
            # Create a new league standing record for the club
            LeagueStanding.objects.create(
                club=club,
                matches_played=0,  # You can set other default values here
                wins=0,
                draws=0,
                losses=0,
                goals_scored=0,
                goals_conceded=0,
                league=league
            )