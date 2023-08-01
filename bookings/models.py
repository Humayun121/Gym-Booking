from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from membership.models import Role

#Holds the bookings with the role, the timestamp and user
class BookingSession(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name

#Validation to check if there are booking slots available
def can_book_session(role,timestamp):
    ammount_booked=BookingSession.objects.filter(role=role, timestamp=timestamp).count()
    if ammount_booked <= role.max_session:
        return True
    else:
        return False

