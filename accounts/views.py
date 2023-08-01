from email import message
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from membership.models import MemberRole
from datetime import datetime, timedelta

def register(request):

    if request.method == 'GET':
        return render(request, 'accounts/register.html')

    #Get form values
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']
    Age = request.POST['Age']
    
    #Checks if age meets the gym criteria
    if int(Age) < 16:
        messages.error(request, 'Age is cannot be less than 16')
        return redirect('register') 

    if int(Age) > 100:
        messages.error(request, 'Age is cannot greater than 100')
        return redirect('register') 
    #Check if passwords match
    if password == password2:
        # Check username
        if User.objects.filter(username=username).exists():
            messages.error(request, 'That username is taken')
            return redirect('register')
        else:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'That email is being used')
                return redirect('register')
            else:
                # Looks good
                user = User.objects.create_user(username=username, password=password, email=email,
                first_name=first_name, last_name=last_name)
                #Login after register
                user.save()
                messages.success(request, 'You are now registered and can log in')
                return redirect('login')
    else:
        messages.error(request, 'Password do not match')   
        return redirect('register')
     
    


def login(request):
    if request.method == 'POST':
        username= request.POST['username']
        password= request.POST['password']
        #user will be authenticated is username and password matches 
        user = auth.authenticate(username=username, password=password)

        #If there is a user then they can be logged in
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
            #if user cannot log in then error message displayed
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
     return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')

def dashboard(request):
    member_roles = MemberRole.objects.filter(user=request.user)
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=7)

    dates =[]
    current_date = start_date
    while current_date < end_date:
        dates.append(current_date)
        current_date = current_date + timedelta(days=1)

    context = {
        'member_roles': member_roles,
        'dates_options': dates,
    }

    return render(request, 'accounts/dashboard.html', context)

    