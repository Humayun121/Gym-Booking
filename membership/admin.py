from django.contrib import admin
from .models import MemberRole, Role

class RoleAdmin(admin.ModelAdmin):
    list_display = ('id','name')

class MemberRoleAdmin(admin.ModelAdmin):
    list_display =('id','user','role')

admin.site.register(MemberRole, MemberRoleAdmin)
admin.site.register(Role, RoleAdmin)