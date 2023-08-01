from django.shortcuts import render
from django.views.generic import ListView
from membership.models import Role, MemberRole

class MembershipView(ListView):
    model = Role
    template_name = 'memberships/list.html'
    def get_user_membership(self):
        user_membership_qs = MemberRole.objects.filter(user=self.request.user)
        if user_membership_qs.exists():
            return user_membership_qs.first()
        return None
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = self.get_user_membership(self.request)
        context['current_membership'] = str(current_membership.membership)
        return context



