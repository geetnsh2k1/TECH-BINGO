from django.urls import path, include
from django.conf.urls import url
from Profile import views
urlpatterns = [
    path('signin/', views.sign_in),
    path('signout/', views.sign_out),
    path('signup/', views.sign_up)
]