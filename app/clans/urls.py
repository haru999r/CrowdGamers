from django.urls import path
from . import views



app_name = 'clans'

urlpatterns = [
    path('', views.home, name='home'),
    path('notice/invite/<str:username>/', views.user_invite_notice, name='user_invite_notice'),
    path('notice/apply/<str:username>/', views.user_apply_notice, name='user_apply_notice'),
    path('clan/create/', views.clan_create, name='clan_create'),
    path('clan/list/', views.clan_list, name='clan_list'),
    path('clan/detail/<int:pk>/', views.clan_detail, name='clan_detail'),
    path('clan/update/<int:pk>/', views.clan_update, name='clan_update'),
    path('clan/delete/<int:pk>/', views.clan_delete, name='clan_delete'),

    # 通知
    path('notice/apply/', views.user_apply_notice, name='user_apply_notice'),
    path('notice/apply/<int:pk>/', views.user_apply_notice_detail, name='user_apply_notice_detail'),
    path('notice/invite/', views.user_invite_notice, name='user_invite_notice'),
    path('notice/invite/<int:pk>/', views.user_invite_notice_detail, name='user_invite_notice_detail'),

    # リクエスト送信
    path('clan/request/input/', views.clan_request_input, name='clan_request_input'),
    path('clan/request/confirm/', views.clan_request_confirm, name='clan_request_confirm'),
    path('clan/request/create/', views.clan_request_create, name='clan_request_create'),

    # 招待送信
    path('invite/input/', views.user_invite_input, name='user_invite_input'),
    path('invite/confirm/', views.user_invite_confirm, name='user_invite_confirm'),
    path('invite/create/', views.user_invite_create, name='user_invite_create'),
]
