from django.urls import path
from . import views
from .views import buy_player

urlpatterns = [
    # URL pattern for the transfer view
    path('transfer/<int:club_id>/', views.transfer_view, name='transfer_view'),
    path('search/', views.player_search, name='player_search'),
    path('buy_player/<int:to_club_id>/', buy_player, name='buy_player'),
]


