from django.urls import path
from . import views


urlpatterns = [
    path('club_selection/', views.club_selection, name='club_selection'),
]