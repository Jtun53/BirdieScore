from django.db import models

# Create your models here.
class Round(models.Model):
    round_id = models.IntegerField(primary_key=True)
    course = None