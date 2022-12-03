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
    path('chatroom',views.chatroom,name='chatroom'),
    path('dashboard',dashboard.as_view(),name='dashboard'),
    path('chat/<int:id>',views.chat,name='chat'),
    path('accounts/logout',views.user_logout,name='logout'),
    path('accounts/reset/password',auth_views.PasswordResetView.as_view(form_class=UserResetPassword,extra_context={'title':'Password Reset'},template_name='panel/password_reset.html'),{'title':'Password Reset'},name='password_reset'),
    path('accounts/reset/password/done',auth_views.PasswordResetDoneView.as_view(template_name='panel/password_reset_done.html'),name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='panel/password_reset_confirm.html'),name='password_reset_confirm'),
    path('reset/password/success',auth_views.PasswordResetCompleteView.as_view(template_name='panel/password_reset_complete.html'),name='password_reset_complete'),
    path('<str:username>',profileView,name='profile'),
    path('edit/<str:username>',EditrofileView.as_view(),name='edit profile'),
    path('change/profile/pic',views.profilePic,name='profile pic'),
    path('account/notifications',views.notifications,name='notifications'),
    path('account/settings',Settings.as_view(),name='settings'),
    path('change/cover/pic',views.coverPic,name='cover pic'),
    path('remove/profile/pic',views.removeProfilePic,name='remove profile pic'),
    path('remove/cover/pic',views.removeCoverPic,name='remove cover pic'),
    path('password/change',views.passwordChange,name='password change'),
    path('action/form',views.actionForm,name='actionform'),
    path('site/settings',EditSite.as_view(),name='site settings'),
    path('site/working/days',views.siteWorking,name='site working days'),
    path('site/contact',views.siteContact,name='site contact'),
    path('site/social/links/settings',views.siteSocial,name='site social links'),
    path('update/status',views.updateStatus,name='update status'),
    path('account/<str:email>',chooseUsername.as_view(),name='choose username'),
    path('welcome/to/the/community',views.WeAreGlad,name='glad to join us'),
    path('request/tweet/form',tweetForm.as_view(),name='tweet form'),
    path('request/comment/form',commentForm.as_view(),name='comment form'),
    path('add/tweet',views.addTweet,name='add form'),
    path('my/messages',accountMessages.as_view(),name='account messages'),
    path('post/like',views.postLike,name='post like'),
    path('post/unlike',views.postUnlike,name='post unlike'),
    path('post/comment',views.postComment,name='post comment'),
    path('user/follow',views.userFollow,name='user follow'),
    path('user/unfollow',views.userUnfollow,name='user unfollow'),
    path('site/users',views.accountUsers,name='users'),
    path('<str:username>/followers',views.accountFollowers,name='followers'),
    path('<str:username>/following',views.accountFollowing,name='following'),
    path('delete/tweet/<int:id>',views.deleteTweet,name='delete tweet'),
    path('posting/comment/like',views.commentLike,name='comment like'),
    path('posting/comment/unlike',views.commentUnlike,name='comment unlike'),
    path('comment/unlike',views.commentUnlike,name='comment unlike'),
    path('user/search',views.userSearch,name='user search'),
    path('delete/comment/<int:id>',views.deleteComment,name='delete comment'),
    path('post/retweet',postRetweet.as_view(),name='post retweet'),
    path('chat/<int:id>',views.chat,name='chat'),
    path('search/chat',views.searchChat,name='search chat'),
    #retrieve/chats
    path('retrieve/chats',views.retrieveChats,name='retrieve chats'),
]

