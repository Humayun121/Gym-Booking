from re import A
from sqlite3 import Timestamp
from time import strftime
from django.shortcuts import render, redirect
from django.urls import reverse
from membership.models import Role, MemberRole
from datetime import datetime, timedelta
from bookings.models import BookingSession
from django.contrib import messages
from bookings.models import can_book_session
from django.core.mail import send_mail 

def bookings(request):
    return render(request, 'bookings/booking.html')


def new_booking(request, role_id, booking_date):
    booking_date_str = booking_date
    booking_date = datetime.strptime(str(booking_date), '%Y%m%d')
    #Current date and time
    start_time = datetime(year=booking_date.year,
                          month=booking_date.month, day=booking_date.day, hour=9)
    end_time = datetime(year=booking_date.year,
                        month=booking_date.month, day=booking_date.day, hour=18)
    #make 1 hour sessions for each hour
    booking_time_options = []
    current_dt = start_time
    while current_dt < end_time:
        role = Role.objects.get(id=role_id)
        if can_book_session(role, current_dt): 
            booking_time_options.append(current_dt)
        current_dt = current_dt + timedelta(hours=1)
        

    if request.method == 'POST':
        role_id = request.POST['role_id']
        booking_date_time_str = request.POST['date_time']
        selected_booking_date_time_str = datetime.strptime(
            booking_date_time_str, '%Y %m %d %H')
        user = request.user
        #Creates a new booking on the database
        booking_session = BookingSession.objects.create(
            #Will take in the user, role_id and the timestamp
            user=user,
            role_id=role_id,
            timestamp=selected_booking_date_time_str
        )

        #Validation for booking
        role = Role.objects.get(id=role_id)
        if can_book_session(role, selected_booking_date_time_str) == True:
            #Save in database
            booking_session.save()
            # Send email
            send_mail(
            'Booking Session',
            'Dear ' + str(booking_session) 
            +', the 1 hour session for '+  str(booking_session.timestamp) + ' has been booked.',
            'codingproject587@gmail.com',
            [user.email, 'codingproject587@gmail.com'],
            fail_silently=False
            )
        else:
            messages.error(request, 'Booking all full')
        return redirect(reverse('bookings'))
    context = {
        'booking_date': booking_date_str,
        'role_id': role_id,
        'booking_dt_options': booking_time_options,
    }
    return render(request, 'bookings/new_book.html', context)


def new_booking_session_manager(request):
    if request.method == 'POST':
        role_id = request.POST['role_id']
        date = request.POST['date']
        # YYYYMMDD
        # March 18, 2022 -> python datetime -> YYYYMMDD

        selected_date_time = datetime.strptime(
            date, '%d %b %Y').strftime('%Y%m%d')

        return redirect(reverse('new_booking', args=[role_id, selected_date_time]))


def index(request):
    #Variable roles will hold all the roles that are in the database
    roles = Role.objects.all()
    # context will return the value of variable using the key 'myroles' 
    context = {
        'myroles': roles
    }
    #render will get back the html page from bookings/index.html
    return render(request, 'bookings/index.html', context)

#When user chooses a membership it links to database 
def role_add(request, role_id):
    user = request.user
    #Validation to check if user already has the same mebership 
    if MemberRole.objects.filter(role_id=role_id, user=user).exists():
        messages.error(request,'Already have this membership')
        return redirect(reverse('bookings'))
    else:
        #Instantiate a new role for a member 
        new_role = MemberRole.objects.create(user=user, role_id=role_id)
        #Saves to database
        new_role.save()
        #redirects user to a new page which is bookings
        return redirect(reverse('bookings'))
