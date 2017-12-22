from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_round/', views.create_round, name='create_round'),
    path('create_course/<str:name>/', views.create_course_by_name, name='create_course_by_name'),
    path('get_course/<str:name>/', views.get_course, name='get_course'),
    path('get_round/<int:id>/', views.get_round_by_id, name ='get_round_by_id'),
    path('add_player/<int:round>/<str:name>', views.add_player_to_round, name='add_player_to_round')
]