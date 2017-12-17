from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_round/', views.create_round, name='create_round'),
]