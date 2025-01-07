from django.shortcuts import render
from .models import Player
from .forms import PlayerSelectionForm

def players_of_desired_club(request, club_name):
    players = Player.objects.filter(club_name=club_name)
    context = {
        'players': players,
        'club_name': club_name,
    }
    return render(request, 'players/players_of_club.html', context)

def player_list_view(request):
    players = Player.objects.all()
    return render(request, 'players/player_list.html', {'players': players})

def select_players_for_match(request):
    form = PlayerSelectionForm()
    if request.method == 'POST':
        form = PlayerSelectionForm(request.POST)
        if form.is_valid():
            selected_players = form.cleaned_data['players']
            # Perform actions with the selected players, such as saving them for the match

    return render(request, 'players/select_players.html', {'form': form})