from django.urls import path
from .views import home_view

urlpatterns = [
    path('homepage/', home_view, name='home'),
]
