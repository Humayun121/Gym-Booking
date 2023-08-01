from django.urls import path

from . import views

#Gives a URL path 
urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
]