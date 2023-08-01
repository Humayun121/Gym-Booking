from django.contrib import admin
from .models import BookingSession

#Display in admin page
class BookingSessionAdmin(admin.ModelAdmin):
    list_display = ('id','role', 'user', 'timestamp')

admin.site.register(BookingSession, BookingSessionAdmin)