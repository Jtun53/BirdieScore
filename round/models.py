from django.db import models
from django.db.models import Q
from random import randint

from round.utils import TimestampModel
# Create your models here.

#figure out what to do when no more available 4 digits.
#also optimize this because it is inefficient when db gets crowded.


class RoundQueryset(models.QuerySet):
    def created_at_interval(self, initial_date, final_date):
        return self.filter(
            Q(created_at__gte=initial_date) &
            Q(created_at__lte=final_date)
        )


def random_4_digits():
    random_number = randint(1000, 9999)
    while True:
        if not Round.objects.filter(round_id=random_number).exists():
            return random_number
        random_number = randint(1000, 9999)


class Course(models.Model):
    course_name = models.CharField(max_length=20)
    hole_1 = models.IntegerField(default=0)
    hole_2 = models.IntegerField(default=0)
    hole_3 = models.IntegerField(default=0)
    hole_4 = models.IntegerField(default=0)
    hole_5 = models.IntegerField(default=0)
    hole_6 = models.IntegerField(default=0)
    hole_7 = models.IntegerField(default=0)
    hole_8 = models.IntegerField(default=0)
    hole_9 = models.IntegerField(default=0)
    hole_10 = models.IntegerField(default=0)
    hole_11 = models.IntegerField(default=0)
    hole_12 = models.IntegerField(default=0)
    hole_13 = models.IntegerField(default=0)
    hole_14 = models.IntegerField(default=0)
    hole_15 = models.IntegerField(default=0)
    hole_16 = models.IntegerField(default=0)
    hole_17 = models.IntegerField(default=0)
    hole_18 = models.IntegerField(default=0)


class Player(models.Model):
    player_name = models.CharField(max_length=50)


class Round(TimestampModel):
    round_id = models.IntegerField(primary_key=True, default=random_4_digits)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)

    objects = RoundQueryset.as_manager()


class Score(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE, default=None)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, default=None)
    hole_1 = models.IntegerField(default=0)
    hole_2 = models.IntegerField(default=0)
    hole_3 = models.IntegerField(default=0)
    hole_4 = models.IntegerField(default=0)
    hole_5 = models.IntegerField(default=0)
    hole_6 = models.IntegerField(default=0)
    hole_7 = models.IntegerField(default=0)
    hole_8 = models.IntegerField(default=0)
    hole_9 = models.IntegerField(default=0)
    hole_10 = models.IntegerField(default=0)
    hole_11 = models.IntegerField(default=0)
    hole_12 = models.IntegerField(default=0)
    hole_13 = models.IntegerField(default=0)
    hole_14 = models.IntegerField(default=0)
    hole_15 = models.IntegerField(default=0)
    hole_16 = models.IntegerField(default=0)
    hole_17 = models.IntegerField(default=0)
    hole_18 = models.IntegerField(default=0)
