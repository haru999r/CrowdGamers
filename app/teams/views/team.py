from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from teams.models import Team, UserProfile
from teams.forms import TeamCreateForm
from .access import OnlyYouMixin, OnlyOwnerMixin
from .utils import GetProfileView



class TeamCreateView(LoginRequiredMixin, CreateView):
    template_name = 'teams/team_create.html'
    model = Team
    form_class = TeamCreateForm
    success_url = reverse_lazy('teams:home')

    def form_valid(self, form):
        """
        チームに所属してなければ作成できる validation つきの保存処理
        """
        profile = self.request.user.user_profile
        if profile.is_owner is True or profile.team:
            form.add_error(None, 'チームは1つまでしか所属できません。')
            return render(self.request, self.template_name, {'form': form})
        result = super().form_valid(form)
        profile.is_owner = True
        profile.team = self.object
        profile.save()
        return result

    def get_success_url(self):
        return reverse('teams:team_detail', kwargs={'teamname': self.object.teamname})

team_create = TeamCreateView.as_view()



class TeamListView(ListView):
    template_name = 'teams/team_list.html'
    model = Team

team_list = TeamListView.as_view()



class TeamUpdateView(LoginRequiredMixin, OnlyOwnerMixin, UpdateView):
    """
    チームプロフィールをアップデートする

    Notes
    -----
    teamname を変更したら URL が Not found になるため success_url は teamname の関係ない URL にする
    """
    template_name = 'teams/team_update.html'
    model = Team
    form_class = TeamCreateForm
    success_url = reverse_lazy('teams:home')

    def form_valid(self, form):
        result = super().form_valid(form)
        self.object = TeamCreateForm(self.request.POST, self.request.FILES, instance=self.request.user.user_profile)
        self.object.save()
        return result

    def get_object(self):
        teamname = self.kwargs.get("teamname")
        return get_object_or_404(Team, teamname=teamname)

team_update = TeamUpdateView.as_view()



class TeamDeleteView(LoginRequiredMixin, OnlyOwnerMixin, DeleteView):
    template_name = 'teams/team_delete.html'
    model = Team
    success_url = reverse_lazy('team:home')

    def get_object(self):
        teamname = self.kwargs.get("teamname")
        return get_object_or_404(Team, teamname=teamname)

team_delete = TeamDeleteView.as_view()



class TeamDetailBaseView(DetailView):
    """
    チームプロフィールの共通部分を表示する
    """
    template_name = 'teams/team_detail.html'
    model = Team
    context_object_name = 'team'

    def get_object(self):
        teamname = self.kwargs.get("teamname")
        return get_object_or_404(Team, teamname=teamname)



class TeamDetailGameView(TeamDetailBaseView):
    template_name = 'teams/team_profile/team_detail.html'
    model = Team

team_detail = TeamDetailGameView.as_view()



class TeamDetailMemberView(TeamDetailBaseView):
    template_name = 'teams/team_profile/team_detail_member.html'
    model = Team

    def get_context_data(self, **kwargs):
        """
        チームに所属しているメンバーを取得する

        Notes
        -----
        owner_profile で一括で取得しようとするとできないので必要なオブジェクトのみ取得
        """
        context = super().get_context_data(**kwargs)
        team = get_object_or_404(Team, teamname=self.kwargs.get("teamname"))
        owner_profile = team.belonging_user_profiles.filter(is_owner=True)[0]
        context['owner_profile_user_username'] = owner_profile.user.username
        context['owner_profile_icon_url'] = owner_profile.icon.url
        context['owner_profile_name'] = owner_profile.name
        return context

team_detail_member = TeamDetailMemberView.as_view()



class TeamDetailFeatureView(TeamDetailBaseView):
    template_name = 'teams/team_profile/team_detail_feature.html'
    model = Team

team_detail_feature = TeamDetailFeatureView.as_view()



class TeamDetailDesiredConditionView(TeamDetailBaseView):
    template_name = 'teams/team_profile/team_detail_desired_condition.html'
    model = Team

team_detail_desired_condition = TeamDetailDesiredConditionView.as_view()



class TeamMemberAddView(TeamDetailBaseView):
    """
    チームのメンバーに追加申請する

    Notes
    -----
    実際の追加処理は他の view で処理を行う
    """
    template_name = 'teams/team_profile/team_member_add.html'
    success_url = 'teams:team_detail'

    def get_object(self):
        teamname = self.kwargs.get("teamname")
        return get_object_or_404(Team, teamname=teamname)

    def get_success_url(self):
        return reverse(self.success_url, kwargs={'teamname': self.object.team.teamname})

team_member_add = TeamMemberAddView.as_view()



class TeamMemberDeleteView(OnlyOwnerMixin, UpdateView):
    """
    チームのメンバーから削除する
    """
    template_name = 'teams/team_profile/team_member_delete.html'
    model = UserProfile
    success_url = 'teams:team_detail'

    def form_valid(self, form):
        """
        プロフィールの team から削除

        TODO
        -----
        プロフィールのチームを削除する処理を書き加える
        """
        result = super().form_valid(form)
        return result

    def get_object(self):
        teamname = self.kwargs.get("teamname")
        return get_object_or_404(Team, teamname=teamname)

    def get_success_url(self):
        return reverse(self.success_url, kwargs={'teamname': self.object.team.teamname})

team_member_delete = TeamMemberDeleteView.as_view()
