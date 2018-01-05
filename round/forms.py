from django import forms
from django.utils.safestring import mark_safe

class RoundForm(forms.Form):
    player_name = forms.CharField(label='Player ID', max_length=100)
    round_id = forms.IntegerField(label='Round ID', required=False)
    course = forms.ChoiceField(choices=(('',''),('Skywest', 'Skywest'),), required=False)
