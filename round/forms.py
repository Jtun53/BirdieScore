from django import forms

class RoundForm(forms.Form):
    player_name = forms.CharField(label='Player ID', max_length=100)
    round_id = forms.IntegerField(label='Round ID')