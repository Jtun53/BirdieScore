from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from .models import Round, Course, Player, Score
from .forms import RoundForm, ScoreForm

# Create your views here.

def index(request):
    form = RoundForm()
    return render(request, 'round/index.html', {'form': form})

#this will be called when a user creates a new round
def create_round(course_name):
    round = Round()
    round.course = Course.objects.get(course_name=course_name)
    round.save()
    return round.round_id

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
        if 'index' in request.POST:
            id = request.POST.get('round_id', '')
            player_name = request.POST.get('player_name')
            player_id = get_player_id_by_name(player_name)
            request.session['_old_post'] = request.POST
        else:
            old_post = request.session.get('_old_post')
            id = old_post.get('round_id', '')
            player_name = old_post.get('player_name', '')
            hole = request.POST.get('hole_num')
            score = request.POST.get('hole_score')
            player_id = get_player_id_by_name(player_name)
            _edit_score(id, player_id, hole, score)
        #if round_id == '' then user got here from Create button
        if id == '':
            course_name = request.POST.get('course')
            id = create_round(course_name)
        else:
            course_name = Round.objects.get(round_id=id).course.course_name
        form = ScoreForm()
        _add_player_to_round(id, player_name)
        if player_id == None:
            player_id = get_player_id_by_name(player_name)
        score_list = []
        scores = get_list_or_404(Score, round_id=id)
        scores[0].par_total = 0
        for items in scores:
            items.total_score = 0
            for x in range(1, 19):
                hole_score = getattr(items, 'hole_{}'.format(x))
                items.total_score += hole_score
                score_list.append("hole {}: {}\n".format(x, hole_score))
                scores[0].par_total += getattr(items.round.course, 'hole_{}'.format(x))
        return render(request, 'round/Scores.html', {'form': form, 'scores': scores, 'player_id': player_id, 'course_name': course_name})

def create_course_by_name(request, name):
    #TODO
    #figoure out how we will assign hole numbers from frontend
    course = Course()
    course.course_name = name
    course.hole_1 = 3
    course.hole_2 = 3
    course.hole_3 = 3
    course.hole_4 = 3
    course.hole_5 = 3
    course.hole_6 = 3
    course.hole_7 = 3
    course.hole_8 = 3
    course.hole_9 = 3

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
    created = False
    if Round.objects.filter(round_id=round_id).exists() == True:
        player_score = Score()
        round = Round.objects.get(round_id=round_id)
        player = Player.objects.filter(player_name=player_name)
        if player.exists() == False:
            new_player = Player()
            new_player.player_name = player_name
            new_player.save()
            player = new_player
        else:
            player = Player.objects.get(player_name=player_name)
        if Score.objects.filter(player_id=player.id).filter(round_id=round_id).exists() == False:
            player_score.round = round
            player_score.player = player
            player_score.save()
            created = True
    return created

def _edit_score(round_id, player_id, hole, score):
    player_score = Score.objects.get(round_id=round_id, player_id=player_id)
    setattr(player_score, 'hole_{}'.format(hole), score)
    player_score.save()

def get_player_id_by_name(name):
    if Player.objects.filter(player_name=name).exists() == True:
        player = Player.objects.get(player_name=name)
        return player.id
    else:
        return None
