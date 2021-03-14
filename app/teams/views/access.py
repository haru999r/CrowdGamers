from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, resolve_url, redirect
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.contrib.auth.mixins import AccessMixin
from teams.models import UserProfile
from accounts.models import User



class OnlyYouMixin(UserPassesTestMixin):
    """
    本人のみアクセスできる Mixin。

    Attributes
    ----------
    raise_exception : bool
        exception を許すかの bool。
    """
    raise_exception = True

    def test_func(self):
        """
        request.user の username がアクセスしようとしている username と同じか確認する

        Returns
        -------
        bool
            True ならアクセス可能
            False ならアクセス不可
        """
        user = self.request.user
        return user.username == self.kwargs['username'] or user.is_superuser



class OnlyOwnerMixin(UserPassesTestMixin):
    """
    チームのオーナーのみアクセスできる Mixin。

    Attributes
    ----------
    raise_exception : bool
        exception を許すかの bool。
    """
    raise_exception = True

    def test_func(self):
        """
        request.user の teamname がアクセスしようとしている teamname と同じか、 request.user はオーナーか確認する

        Returns
        -------
        bool
            True ならアクセス可能
            False ならアクセス不可
        """
        user = self.request.user
        if user.is_authenticated:
            return user.user_profile.is_owner == True and user.user_profile.team.teamname == self.kwargs.get('teamname') or user.is_superuser
        else:
            return False



class CustomAccessMixin(AccessMixin):
    """
    AnonymousUser のみのアクセスに対応した Mixin を作成するため AccessMixin をカスタムしたクラス。
    親クラスと違うのは get_home_url の名前、 handle_no_permission の処理。
    """
    home_url = None

    def get_home_url(self):
        """
        AnonymousUser なら、 self.home_url もしくは 孫クラスの home_url にリダイレクトする関数。

        Raises
        ------
        ImproperlyConfigured
            ログインユーザーがアクセスした時にリダイレクトさせる URL がないため。

        Returns
        -------
        redirect(home_url) : Callable
            孫クラスで定義した home_url もしくは、 settings.LOGIN_REDIRECT_URL で定義した urlにリダイレクト。
        """
        home_url = self.home_url or settings.LOGIN_REDIRECT_URL
        if not home_url:
            raise ImproperlyConfigured(
                '{0} is missing the home_url attribute. Define {0}.home_url, settings.LOGIN_REDIRECT_URL, or override '
                '{0}.get_home_url().'.format(self.__class__.__name__)
            )
        return redirect(home_url)

    def handle_no_permission(self):
        """
        permission がないユーザーの画面処理。

        Parameters
        ----------
        self.raise_exception : bool
            孫クラスで定義。 raise_exception を許すかどうか。

        Returns
        -------
        self.get_home_url() : Callable
            同クラスの get_home_url 関数。

        Raises
        ------
        PermissionDenied
            raise_exception True か request.user が未ログインのため。
            普通なら anonymous_user がこの処理を通ることはない（小クラスの dispatch 関数で anonymous_user がこの関数の処理を通らないようにしているため）。
        """
        if self.raise_exception or self.request.user.is_anonymous:
            raise PermissionDenied(self.get_permission_denied_message())
        return self.get_home_url()



class AnonymousRequiredMixin(CustomAccessMixin):
    """
    AnonymousUser のみアクセスできる Mixin。

    Examples
    --------
    AnonymousRequiredMixin を継承するのみで使用可能。
    home_url は任意

    class SampleView(AnonymousRequiredMixin, TemplateView):
        home_url = 'views.home'
        # more ...
    """

    def dispatch(self, request, *args, **kwargs):
        """
        request.user はアクセス権限があるか判断する。
        ログインユーザーはアクセスできない。

        Returns
        -------
        self.handle_no_permission : Callable
            親クラスの handle_no_permission 関数。
        super().dispatch(request, *args, **kwargs)
            親クラス(CustomAccessMixin)の dispatch 関数。
        """
        if request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
