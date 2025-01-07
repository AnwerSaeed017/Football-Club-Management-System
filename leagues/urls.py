from django.urls import path
from . import views


urlpatterns = [
    path('league_selection/', views.league_selection, name='league_selection'),
    path('league_standing/', views.league_standings_view, name='league_standing'),
]