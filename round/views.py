from django.shortcuts import render
from django.http import HttpResponse
from .models import Round, Course, Player

# Create your views here.

def index(request):
    return HttpResponse('test')

#this will be called when a user creates a new round
def create_round(request):
    round = Round()
    round.course = Course.objects.get(course_name='Skywest')
    round.save()
    return HttpResponse('Created')

def add_player_to_round(request, round, name):
    round = Round.objects.get(round_id=round)
    for x in range (1,4):
        if getattr(round,'player_{}'.format(x)) != None:
            round.player_1 = Player()
            round.player_1.player_name = name
            round.player.save()
    return HttpResponse("Created player")

def get_round_by_id(request, id):
    round = Round.objects.get(round_id=id)
    return HttpResponse(getattr(round, 'player_1'))

def create_course_by_name(request, name):
    #TODO
    #figoure out how we will assign hole numbers from frontend
    course = Course()
    course.course_name = name
    course.hole_1 = 5
    course.hole_2 = 4
    course.hole_3 = 4
    course.hole_4 = 5
    course.hole_5 = 3
    course.hole_6 = 4
    course.hole_7 = 4
    course.hole_8 = 3
    course.hole_9 = 4
    course.hole_10 = 4
    course.hole_11 = 4
    course.hole_12 = 3
    course.hole_13 = 4
    course.hole_14 = 5
    course.hole_15 = 4
    course.hole_16 = 3
    course.hole_17 = 5
    course.hole_18 = 4

    course.save()

    return HttpResponse("CREATED")

def get_course(request, name):
    course = Course.objects.get(course_name=name)
    info = []
    info.append('Course_name: {}\n'.format(getattr(course, 'course_name')))
    for x in range(1,19):
        info.append('Hole {}: {}\n'.format(x, getattr(course, 'hole_{}'.format(x))))
    return HttpResponse("".join(info))

def get_score(request,round_id, name):
    pass

def edit_score(request,round_id, name, hole, num):
    pass