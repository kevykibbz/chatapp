from django.urls import path
from django import views
from . import views
from .views import *
from .forms import UserResetPassword
from django.contrib.auth import views as auth_views


urlpatterns=[
    path('',Home.as_view(),name='home'),
    path('accounts/login/',Home.as_view(),name='home'),
    path('register',views.register,name='register'),
    path('chatroom',views.chatroom,name='dashboard'),
    path('chat/<int:id>',views.chat,name='chat'),
    path('accounts/logout',views.user_logout,name='logout'),
    path('accounts/reset/password',auth_views.PasswordResetView.as_view(form_class=UserResetPassword,extra_context={'title':'Password Reset'},template_name='panel/password_reset.html'),{'title':'Password Reset'},name='password_reset'),
    path('accounts/reset/password/done',auth_views.PasswordResetDoneView.as_view(template_name='panel/password_reset_done.html'),name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='panel/password_reset_confirm.html'),name='password_reset_confirm'),
    path('reset/password/success',auth_views.PasswordResetCompleteView.as_view(template_name='panel/password_reset_complete.html'),name='password_reset_complete'),
    path('<str:username>',ProfileView.as_view(),name='profile'),
    path('change/profile/pic',views.profilePic,name='profile pic'),
    path('password/change',views.passwordChange,name='password change'),
    path('action/form',views.actionForm,name='actionform'),
    path('site/settings',EditSite.as_view(),name='site settings'),
    path('site/working/days',views.siteWorking,name='site working days'),
    path('site/contact',views.siteContact,name='site contact'),
    path('site/social/links/settings',views.siteSocial,name='site social links'),
    path('update/status',views.updateStatus,name='update status'),
]

