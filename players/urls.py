from django.urls import path
from .views import players_of_desired_club
from .views import player_list_view
from .views import select_players_for_match

urlpatterns = [
    path('club/<str:club_name>/', players_of_desired_club, name='players_of_club'),
    path('', player_list_view, name='player_list'),
    path('select-players/', select_players_for_match, name='select_players_for_match'),
    # Other URL patterns if needed
]
