from django.shortcuts import render, get_object_or_404, redirect
from .models import Player, ClubFinances, PlayerTransfer, FootballClub
from players.models import PlayerClubAssociation,PlayerAttribute
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from signupuser.models import UserLeagueClubSelection

def transfer_view(request, club_id):
    user_club = get_object_or_404(FootballClub, id=club_id)
    club_finances = get_object_or_404(ClubFinances, club=user_club)

    # Retrieve players available for transfer with their market value
    players_associations = PlayerClubAssociation.objects.exclude(club=user_club)
    players_available = [
        {
            'player': association.player,
            'market_value': association.market_value
        }
        for association in players_associations
    ]

    transfers_made = PlayerTransfer.objects.filter(from_club=user_club) | PlayerTransfer.objects.filter(to_club=user_club)

    if request.method == 'POST':
        player_id = request.POST.get('player_id')
        association_to_buy = get_object_or_404(PlayerClubAssociation, player_id=player_id)

        if association_to_buy.market_value <= club_finances.available_funds:
            # Update club finances
            club_finances.available_funds -= association_to_buy.market_value
            club_finances.save()

            # Create transfer record
            PlayerTransfer.objects.create(
                player=association_to_buy.player,
                from_club=association_to_buy.club,
                to_club=user_club,
                transfer_fee=association_to_buy.market_value
            )

            # Update player's club in PlayerClubAssociation
            association_to_buy.club = user_club
            association_to_buy.save()

            # Update the player's club in the Player model
            player = association_to_buy.player
            player.club_name = user_club.name 
            player.save()

            # Redirect to refresh the page and show the updated info
            selected_club = FootballClub.objects.get(id=club_id)
            return redirect('players_of_club', selected_club)

    return render(request, 'transfer/transfer.html', {
        'user_club': user_club,
        'club_finances': club_finances,
        'players_available': players_available,
        'transfers_made': transfers_made
    })


def player_search(request):
    query_name = request.GET.get('name', '')
    query_position = request.GET.get('position', '')

    # Retrieve the latest UserLeagueClubSelection for the user
    user_club_selection = UserLeagueClubSelection.objects.filter(user=request.user).order_by('-selection_date').first()

    # Check if a UserLeagueClubSelection exists for the user
    if user_club_selection:
        user_club_id = user_club_selection.club.id
    else:
        user_club_id = None

    if query_name:
        players = Player.objects.filter(name__icontains=query_name)
    elif query_position:
        players = Player.objects.filter(position__icontains=query_position)
    else:
        players = Player.objects.none()

    players_data = []

    for player in players:
        player_data = {
            'name': player.name,
            'position': player.position,
            'age': player.age,
            'nationality': player.nationality,
            'club_id': user_club_id,
            'club_name': player.club_name,
            'image_url': player.image_url,
        }

        # Fetch market value
        player_association = PlayerClubAssociation.objects.filter(player=player).first()
        player_data['market_value'] = player_association.market_value if player_association else "Not Available"

        # Fetch player attributes
        player_attributes = PlayerAttribute.objects.filter(player=player).first()

        if player_attributes:
            player_data.update({
                'id': player.id,  # Access the player's ID directly
                'speed': player_attributes.speed,
                'strength': player_attributes.strength,
                'stamina': player_attributes.stamina,
                'agility': player_attributes.agility,
                'passing': player_attributes.passing,
                'dribbling': player_attributes.dribbling,
                'shooting': player_attributes.shooting,
                'heading': player_attributes.heading,
                'tackling': player_attributes.tackling,
                'positioning': player_attributes.positioning,
                'vision': player_attributes.vision,
                'composure': player_attributes.composure,
                'crossing': player_attributes.crossing,
                'finishing': player_attributes.finishing,
                'freekicks': player_attributes.freekicks,
            })
        else:
            # Set default values if no attributes found
            attributes = ['speed', 'strength', 'stamina', 'agility', 'passing', 'dribbling', 'shooting', 'heading', 'tackling', 'positioning', 'vision', 'composure', 'crossing', 'finishing', 'freekicks']
            for attr in attributes:
                player_data[attr] = "Not Available"

        players_data.append(player_data)

    return render(request, 'search.html', {'players': players_data})



def buy_player(request, to_club_id):
    try:
        to_club_id = int(to_club_id)
    except ValueError:
        # Handle the error, maybe redirect or show an error message
        messages.error(request, "Invalid club ID.")
        return redirect('players_of_club')

# Extract and validate player_id
    player_id = request.POST.get('player_id')
    try:
        player_id = int(player_id)
    except ValueError:
    # Handle the error
        messages.error(request, "Invalid player ID.")
        return redirect('players_of_club')
    
    # Continue with your existing logic
    player = get_object_or_404(Player, id=player_id)
    to_club = get_object_or_404(FootballClub, id=to_club_id)
    some_club_name=to_club.name
    # Get the current club association and finances for the buying club
    current_association = PlayerClubAssociation.objects.get(player=player)
    buying_club_finances = ClubFinances.objects.get(club=to_club)

    # Check if the buying club has enough funds
    if buying_club_finances.available_funds < current_association.market_value:
        messages.error(request, "The club does not have enough funds to buy this player.")
        return redirect('players_of_club',club_name=some_club_name)

    with transaction.atomic():
        # Update the finances of the buying club
        buying_club_finances.available_funds -= current_association.market_value
        buying_club_finances.save()

        # Create a transfer record
        PlayerTransfer.objects.create(
            player=player,
            from_club=current_association.club,
            to_club=to_club,
            transfer_fee=current_association.market_value
        )

        # Update the player's club association
        current_association.club = to_club
        current_association.save()

        # Update the player's club in the Player model
        player = current_association.player
        player.club_name = some_club_name 
        player.save()

        messages.success(request, f"You have successfully bought {player.name}.")

    return redirect('players_of_club',club_name=some_club_name)