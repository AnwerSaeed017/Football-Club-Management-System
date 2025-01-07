from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('signup/', views.signup, name='signup'),
     path('', views.login, name='login'),
]