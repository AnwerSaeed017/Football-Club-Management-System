from django.contrib import admin
from .models import Player, PlayerAttribute  # Import your models

# Register your models here.
admin.site.register(Player)
admin.site.register(PlayerAttribute)
