from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from signupuser.models import UserLeagueClubSelection
from schedule.models import MatchSchedule

def home_view(request):
    if request.user.is_authenticated:
        user_selection = UserLeagueClubSelection.objects.filter(user=request.user).first()
        if user_selection:
            selected_club = user_selection.club

            # Find the next scheduled match for the selected club
            next_scheduled_match = MatchSchedule.objects.filter(
                Q(home_team=selected_club) | Q(away_team=selected_club),
                match_occurred=False
            ).order_by('match_date')

            context = {
                'selected_club': selected_club,
                'matches': next_scheduled_match,  # Pass the queryset of matches
            }
            return render(request, 'home/homepage.html', context)
        else:
            # Redirect to club selection if no club is selected
            return redirect('club_selection')
    else:
        # Redirect to login if the user is not authenticated
        return redirect('login')
