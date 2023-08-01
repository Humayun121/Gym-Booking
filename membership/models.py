from django.db import models
from django.contrib.auth.models import User

#class will hold the different type of membership
class Role(models.Model):
    name = models.CharField(max_length=30, unique=True)
    max_session = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.name

#Class links the user with the role they chose
class MemberRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} {self.role}'


# create table member_role(
#     id serial primary key,
#     user_id int constraints foreign key on auth_user.id,
#     role_id int constraint foeign key on role.id
# )