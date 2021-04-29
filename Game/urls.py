from django.urls import path, include
from django.conf.urls import url
from Game import views

urlpatterns = [
    path('play/<str:username>/', views.game_home, name='g_home'),
    path('play/<str:username>/save/', views.save),
    path('play/<str:username>/main/', views.play, name='main'),
    path('play/<str:username>/main/input/', views.update),
]