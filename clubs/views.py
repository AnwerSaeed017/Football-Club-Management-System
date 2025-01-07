from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from signupuser.models import UserLeagueClubSelection
from leagues.models import League
from clubs.models import FootballClub
from match.models import MatchSchedule
from leagues.views import insert_clubs_into_leaguestanding
from sample import schedule_matches_for_league
from club_finances import assign_random_finances

def club_selection(request):
    if request.user.is_authenticated:
        selected_league_id = request.session.get('selected_league_id')
        if not selected_league_id:
            return redirect('league_selection')  # Redirect to league selection if no league is chosen

        clubs = FootballClub.objects.filter(leagues__id=selected_league_id)

        if request.method == 'POST':
            selected_club_id = request.POST.get('club')
            selected_club = FootballClub.objects.get(id=selected_club_id)
            selected_league = League.objects.get(id=selected_league_id)
            
            # Save the user's club selection
            UserLeagueClubSelection.objects.update_or_create(
                user=request.user,
                defaults={'league': selected_league, 'club': selected_club, 'selection_date': timezone.now()}
            )

            # Insert all clubs into league standing table
            insert_clubs_into_leaguestanding(selected_league_id)

            # Find the next scheduled match for the selected club
            next_scheduled_match = MatchSchedule.objects.filter(
                match_occurred=False, home_team=selected_club
            ).order_by('match_date').first()

            messages.success(request, 'Club selection successful!')
            
            league_name = selected_league.name  # Replace with your league name
            schedule_matches_for_league(league_name)
            assign_random_finances()

            return render(request, 'clubs/club_selection_success.html', {
                'selected_club': selected_club,
                'next_match': next_scheduled_match
            })

        return render(request, 'clubs/club_selection.html', {'clubs': clubs})
    else:
        return redirect('home')
