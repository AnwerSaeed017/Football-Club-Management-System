from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from schedule.models import MatchSchedule
from leagues.models import LeagueStanding
from match.models import MatchResult
import random
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class match_schedule_view(View):  # Rename the class
    def get(self, request):
        selected_league_id = request.session.get('selected_league_id')

        if not selected_league_id:
            # If no league is selected, redirect to league selection or handle appropriately
            return redirect('league_selection')
        matches = MatchSchedule.objects.filter(league_id=selected_league_id)
        return render(request, 'schedule/match_schedule.html', {'matches': matches})

class GenerateMatchResult(View):
    @method_decorator(login_required)
    def post(self, request):
        next_scheduled_match = MatchSchedule.objects.filter(match_occurred=False).order_by('match_date').first()

        if not next_scheduled_match:
            return render(request, 'no_upcoming_matches.html')

        existing_result = MatchResult.objects.filter(match=next_scheduled_match).exists()
        if existing_result:
            return render(request, 'match_result_exists.html', {'scheduled_match': next_scheduled_match})

        home_team_goals = random.randint(0, 5)
        away_team_goals = random.randint(0, 5)

        match_result = MatchResult.objects.create(
            match=next_scheduled_match,
            user=request.user,
            home_team_goals=home_team_goals,
            away_team_goals=away_team_goals,
            match_date=next_scheduled_match.match_date
        )

        update_league_standing(next_scheduled_match.home_team, home_team_goals, away_team_goals, match_result)
        update_league_standing(next_scheduled_match.away_team, away_team_goals, home_team_goals, match_result)

        next_scheduled_match.match_occurred = True
        next_scheduled_match.save()

        return render(request, 'generated_match_result.html', {'match_result': match_result})

class GenerateMatchResultOfOurClub(View):
    @method_decorator(login_required)
    def post(self, request):
        match_id = request.POST.get('match_id')
        next_scheduled_match = MatchSchedule.objects.filter(id=match_id, match_occurred=False).first()

        if not next_scheduled_match:
            return render(request, 'no_upcoming_matches.html')

        existing_result = MatchResult.objects.filter(match=next_scheduled_match).exists()
        if existing_result:
            return render(request, 'match_result_exists.html', {'scheduled_match': next_scheduled_match})

        home_team_goals = random.randint(0, 5)
        away_team_goals = random.randint(0, 5)

        match_result = MatchResult.objects.create(
            match=next_scheduled_match,
            user=request.user,
            home_team_goals=home_team_goals,
            away_team_goals=away_team_goals,
            match_date=next_scheduled_match.match_date
        )

        update_league_standing(next_scheduled_match.home_team, home_team_goals, away_team_goals, match_result)
        update_league_standing(next_scheduled_match.away_team, away_team_goals, home_team_goals, match_result)
        resultofothermatches(match_id,request.user)
        next_scheduled_match.match_occurred = True
        next_scheduled_match.save()

        return render(request, 'generated_match_result.html', {'match_result': match_result})

def update_league_standing(team, goals_for, goals_against, match_result):
    standing, created = LeagueStanding.objects.get_or_create(league=match_result.match.league, club=team)

    standing.goals_scored += goals_for
    standing.goals_conceded += goals_against

    if goals_for > goals_against:
        standing.wins += 1
        standing.points += 3
    elif goals_for == goals_against:
        standing.draws += 1
        standing.points += 1
    else:
        standing.losses += 1

    standing.matches_played += 1
    standing.points_difference = standing.goals_scored - standing.goals_conceded

    standing.save()

def resultofothermatches(match_id,user):
    # Get the specified match and all previous unscheduled matches
    target_match = get_object_or_404(MatchSchedule, id=match_id)
    unscheduled_matches = MatchSchedule.objects.filter(match_occurred=False, match_date__lte=target_match.match_date).order_by('match_date')

    for match in unscheduled_matches:
        existing_result = MatchResult.objects.filter(match=match).exists()
        if not existing_result:
            home_team_goals = random.randint(0, 5)
            away_team_goals = random.randint(0, 5)

            match_result = MatchResult.objects.create(
                match=match,
                user=user,
                home_team_goals=home_team_goals,
                away_team_goals=away_team_goals,
                match_date=match.match_date
            )

            update_league_standing(match.home_team, home_team_goals, away_team_goals, match_result)
            update_league_standing(match.away_team, away_team_goals, home_team_goals, match_result)

            match.match_occurred = True
            match.save()