from django.urls import path

from .import views

urlpatterns = [
    path('', views.index, name='bookings'),
    path('<int:booking_id>', views.bookings, name='booking'),
    path('role/<int:role_id>', views.role_add, name='role_add'),  
    path('new_book/<int:role_id>/<int:booking_date>', views.new_booking, name='new_booking'),
    path('new_book/session_manager/', views.new_booking_session_manager, name='new_booking_session_manager'),
]

