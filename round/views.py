from django.shortcuts import render
from django.http import HttpResponse
from .models import Round

# Create your views here.

def index(request):
    return HttpResponse('test')

#this will be called when a user creates a new round
def create_round(request):
    round = Round()
    round.save()
    return HttpResponse("Created")