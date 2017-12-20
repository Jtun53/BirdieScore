from django.test import TestCase
from .models import Round

# Create your tests here.
class RoundModelTests(TestCase):

    def test_create_round(self):
        """If a round is created, it should be in the database"""
        round = Round()
        round.save()
        self.assertIs(Round.objects.all().count(), 1)

    def test_get_round(self):
        """If an entry in the database is queried, should return true if it exists"""
        round = Round()
        round.save()
        created_id = round.round_id
        #entry = Round.objects.get(round_id=created_id)
        self.assertIs(Round.objects.filter(round_id=round.round_id).exists(), True)

    def test_get_round_not_in_db(self):
        """If an entry in the database is queried, should return false if it does not exist"""
        round = Round()
        round.save()
        created_id = round.round_id
        #entry = Round.objects.get(round_id=created_id)
        self.assertIs(Round.objects.filter(round_id=-1).exists(), False)

    def test_round_specific_id(self):
        round = Round()
        round.round_id = 1234
        round.save()
        self.assertIs(Round.objects.filter(round_id=1234).exists(), True)

