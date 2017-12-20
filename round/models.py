from django.db import models
from random import randint

# Create your models here.

#figure out what to do when no more available 4 digits.
#also optimize this because it is inefficient when db gets crowded.
def random_4_digits():
    random_number = randint(1000, 9999)
    while True:
        if not Round.objects.filter(round_id=random_number).exists():
            return random_number
        random_number = randint(1000, 9999)

class Round(models.Model):
    round_id = models.IntegerField(primary_key=True, default=random_4_digits)
    course = None