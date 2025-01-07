from django import forms
from .models import Player

class PlayerSelectionForm(forms.Form):
    players = forms.ModelMultipleChoiceField(queryset=Player.objects.all(), widget=forms.CheckboxSelectMultiple)
