from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, CreateView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import Q
from accounts.models import User
from teams.models import Team, Invite, Apply, UserProfile
from teams.forms import InviteCreateForm, ApplyCreateForm
from teams.views import OnlyYouMixin



""" 通知関連 view """

class InviteNotificationView(LoginRequiredMixin, OnlyYouMixin, TemplateView):
    template_name = 'teams/notification/invite_notification.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['invitation'] = Invite.objects.filter(
            Q(from_user=self.request.user) |
            Q(to_user=self.request.user)
        ).order_by('-created_at')
        return ctx

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

invite_notification = InviteNotificationView.as_view()



class InviteNotificationDetailView(LoginRequiredMixin, OnlyYouMixin, DetailView):
    template_name = 'teams/notification/invite_notification_detail.html'
    model = Invite

    def get_object(self):
        return get_object_or_404(UserProfile, user=self.kwargs.get('user'))

invite_notification_detail = InviteNotificationDetailView.as_view()



class ApplyNotificationView(LoginRequiredMixin, OnlyYouMixin, TemplateView):
    template_name = 'teams/notification/apply_notification.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['application'] = Apply.objects.filter(
            Q(from_user=self.request.user) |
            Q(to_user=self.request.user)
        ).order_by('-created_at')
        return ctx

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

apply_notification = ApplyNotificationView.as_view()



class ApplyNotificationDetailView(LoginRequiredMixin, OnlyYouMixin, DetailView):
    template_name = 'teams/notification/apply_notification_detail.html'
    model = Apply

    def get_object(self):
        return get_object_or_404(UserProfile, user=self.kwargs.get('user'))

apply_notification_detail = ApplyNotificationDetailView.as_view()
