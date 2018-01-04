from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Round, Course, Player, Score
from .forms import RoundForm

# Create your views here.

def index(request):
    form = RoundForm()
    return render(request, 'round/index.html', {'form': form})

#this will be called when a user creates a new round
def create_round(request):
    round = Round()
    round.course = Course.objects.get(course_name='Skywest')
    round.save()
    return HttpResponse('Created')

def create_player(request, id):
    if Player.objects.filter(player_name=id).exists() == False:
        new_player = Player()
        new_player.player_name = id
        new_player.save()
        response = "Created Player"
    else:
        response = "Player already exists!"
    return HttpResponse(response)

def get_round_by_id(request):
    if request.method == 'POST':
        id = request.POST.get('round_id','')
        score_list = []
        scores = Score.objects.filter(round_id=id)
        for items in scores:
            for x in range(1, 19):
                hole_score = getattr(items, 'hole_{}'.format(x))
                score_list.append("hole {}: {}\n".format(x, hole_score))
        return HttpResponse("\n".join(score_list))

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
    for x in range(1, 19):
        info.append('Hole {}: {}\n'.format(x, getattr(course, 'hole_{}'.format(x))))
    return HttpResponse("".join(info))

def get_score(request, round_id, player_id):
    player_score = Score.objects.filter(round_id=round_id)
    HttpResponse(str(player_score))

def _add_player_to_round(round_id, player_name):
    if Round.objects.filter(round_id=round_id).exists() == False:
       return 0
    else:
        player_score = Score()
        round = Round.objects.get(round_id=round_id)
        if Player.objects.filter(player_name=player_name).exists() == False:
            new_player = Player()
            new_player.player_name = player_name
            new_player.save()
            player = new_player
        else:
            player = Player.objects.get(player_name=player_name)
        player_score.round = round
        player_score.player = player
        player_score.save()
        return 1

def edit_score(request, round_id, player_name, hole, score):
    if Score.objects.filter(round_id=round_id).exists() == False or Player.objects.filter(player_name=player_name).exists() == False:
        success = _add_player_to_round(round_id, player_name)
        if success:
            new_player_id = Player.objects.get(player_name=player_name)
            player_score = Score.objects.get(round_id=round_id, player_id=new_player_id)
            setattr(player_score, 'hole_{}'.format(hole), score)
            player_score.save()
            return HttpResponse("Score edited")
        else:
            return HttpResponse("Error editing score!")

    #The player already has an existing entry for the current round
    else:
        player_id = Player.objects.get(player_name=player_name)
        player_score = Score.objects.get(round_id=round_id, player_id=player_id)
        setattr(player_score, 'hole_{}'.format(hole), score)
        player_score.save()
        return HttpResponse('Score for {} updated'.format(player_name))
