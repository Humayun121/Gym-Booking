from django.shortcuts import render
from django.http import HttpResponse

#Gives back the index.html file
def index(request):
    return render(request, 'pages/index.html')


#Gives back the about.html file
def about(request):
    return render(request, 'pages/about.html')

