from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from .models import Round, Course, Player, Score, RoundQueryset
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

def generate_player_scores(request, player_name, course_name):
    player_id = get_player_id_by_name(player_name)
    score_list = Score.objects.filter(player_id=player_id).filter(round__course__course_name=course_name)
    course_score = Course.objects.get(course_name=course_name)
    for x in range(len(score_list)):
        if score_list[x].round.course.course_name != course_name:
            del score_list[x]                                                 
    course_total = 0
    count = 0
    for score in score_list:
        round_tot = 0
        for x in range(1, 19):
            round_tot += getattr(score, 'hole_{}'.format(x))
        score_list[count].round_tot = round_tot
        count += 1


    for x in range(1, 19):
        hole_score = getattr(course_score, 'hole_{}'.format(x))
        course_total += hole_score
    course_score.par_total= course_total
    return render(request, 'round/player_score_list.html', {'score_list': score_list,
                                                            'player_name': player_name,
                                                            'course_score': course_score})

def get_round_by_id(request):
    if request.method == 'POST':
        if 'get_scores' in request.POST:
            player_name = request.POST.get('player_name')
            course_name = request.POST.get('course')
            return generate_player_scores(request, player_name, course_name)
        elif 'index' in request.POST:
            id = request.POST.get('round_id', '')
            player_name = request.POST.get('player_name')
            player_id = get_player_id_by_name(player_name)
            request.session['_old_post'] = request.POST
        else:
            old_post = request.session.get('_old_post')
            id = old_post.get('round_id', '')
            if id == '':
                id = request.session['generated_id']
            player_name = old_post.get('player_name', '')
            hole = request.POST.get('hole_num')
            score = request.POST.get('hole_score')
            player_id = get_player_id_by_name(player_name)
            _edit_score(id, player_id, hole, score)
        #if round_id == '' then user got here from Create button
        if id == '':
            course_name = request.POST.get('course')
            id = create_round(course_name)
            request.session['generated_id'] = id
            course = Round.objects.get(round_id=id).course
        else:
            course = Round.objects.get(round_id=id).course
        form = ScoreForm()
        _add_player_to_round(id, player_name)
        if player_id == None:
            player_id = get_player_id_by_name(player_name)
        score_list = []
        scores = get_list_or_404(Score, round_id=id)
        form['hole_num'].initial = set_next_empty_hole(player_id, scores)
        scores[0].par_total = 0
        for items in scores:
            items.total_score = 0
            for x in range(1, 19):
                hole_score = getattr(items, 'hole_{}'.format(x))
                items.total_score += hole_score
                score_list.append("hole {}: {}\n".format(x, hole_score))
        for x in range(1, 19):
            scores[0].par_total += getattr(scores[0].round.course, 'hole_{}'.format(x))

        return render(request, 'round/Scores.html', {'form': form, 'scores': scores, 'player_id': player_id, 'course': course})

def set_next_empty_hole(player_id, scores):
    for player_scores in scores:
        if player_scores.player.id == player_id:
            for i in range(1,19):
                if getattr(player_scores, 'hole_{}'.format(i)) == 0:
                    return (i,i)
            return ()


def create_course_by_name(request, name):
    #TODO
    #figoure out how we will assign hole numbers from frontend
    course = Course()
    course.course_name = name
    course.hole_1 = 3
    course.hole_2 = 4
    course.hole_3 = 3
    course.hole_4 = 4
    course.hole_5 = 4
    course.hole_6 = 3
    course.hole_7 = 4
    course.hole_8 = 3
    course.hole_9 = 4

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
