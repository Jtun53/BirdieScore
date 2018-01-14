from django import forms
from django.utils.safestring import mark_safe

class RoundForm(forms.Form):
    player_name = forms.CharField(label='Player ID', max_length=100)
    round_id = forms.IntegerField(label='Round ID', required=False)
    course = forms.ChoiceField(choices=(('', ''), ('Skywest', 'Skywest'), ('Mariner\'s Point', 'Mariner\'s Point'), ('Fremont Park', 'Fremont Park')), required=False)

class ScoreForm(forms.Form):
    hole_num = forms.ChoiceField(label="Hole Number", choices=((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10),
                                          (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18)))

    hole_score = forms.ChoiceField(label="Hole Score", choices=((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)))