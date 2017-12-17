from django.db import models
from random import randint

# Create your models here.
def random_4_digits():
    return randint(1000, 9999)

class Round(models.Model):
    round_id = models.IntegerField(primary_key=True, default=random_4_digits)
    course = None