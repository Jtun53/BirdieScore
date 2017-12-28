from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_round/', views.create_round, name='create_round'),
    path('create_course/<str:name>/', views.create_course_by_name, name='create_course_by_name'),
    path('get_course/<str:name>/', views.get_course, name='get_course'),
    path('get_round/<int:id>/', views.get_round_by_id, name='get_round_by_id'),
    path('create_player/<str:id>', views.create_player, name='create_player'),
    path('get_score/<int:round_id>', views.get_score, name='get_score'),
    path('create_player/<str:id>', views.create_player, name='create_player'),
    path('edit_score/<int:round_id>/<str:player_name>/<int:hole>:<int:score>', views.edit_score, name='edit_score')
]