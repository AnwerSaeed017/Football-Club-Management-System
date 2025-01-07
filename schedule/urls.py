from django.urls import path
from .views import match_schedule_view  # Import the renamed class
from .views import GenerateMatchResult
from .views import GenerateMatchResultOfOurClub

urlpatterns = [
    path('schedule/', match_schedule_view.as_view(), name='match_schedule'),  # Use the renamed class


    # URL for displaying match result exists
    path('generate_match_result/', GenerateMatchResult.as_view(), name='generate_match_result'),
    
     path('generate_result/', GenerateMatchResultOfOurClub.as_view(), name='generate_result'),
]
