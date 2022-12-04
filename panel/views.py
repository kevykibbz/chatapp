from django.shortcuts import render
from django.http import JsonResponse,HttpResponse,HttpResponseBadRequest
from django.shortcuts import render,get_object_or_404,redirect
from asgiref.sync import sync_to_async
from installation.models import SiteModel
import time,asyncio
from django.contrib.humanize.templatetags.humanize import intcomma,naturaltime
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from .decorators import unauthenticated_user,allowed_users
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from .search import searchUser
from.utils import get_current_writers
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
import json
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from rest_framework.decorators import api_view
import re
from django.contrib.auth import update_session_auth_hash
from channels.layers import get_channel_layer
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password
from django.db.models import Avg
import timeago,datetime
from  django.contrib.auth.models import Group
from datetime import timedelta
from .serializers import *
import os
from datetime import date
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
todays_date=date.today()
# Create your views here.

def generate_id():
    return get_random_string(5,'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKMNOPQRSTUVWXYZ0123456789')

    
def check_data():
    if SiteModel.objects.count() > 0:
        obj=SiteModel.objects.all()[0]
        return obj


#chooseUsername
class chooseUsername(View):
    def get(self,request,email):
        obj=check_data()
        if not obj:
            return redirect('/installation/')
        user=get_object_or_404(User,email__exact=email)
        form=ChooseForm(instance=user)
        data={
            'title':'Choose Username',
            'form':form,
            'data':request.user,
            'obj':obj,
        }
        return render(request,'panel/choose_username.html',context=data)
    def post(self,request,email,*args , **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            user=get_object_or_404(User,email__exact=email)
            form=ChooseForm(request.POST or None , instance=user)
            if form.is_valid():
                usr=form.save()
                user=authenticate(username=usr.username,password=user.extendedauthuser.temporary_password)
                if user is not None:
                    login(request,user)
                    user.extendedauthuser.temporary_password=None
                    user.save()
                return JsonResponse({'valid':True,'message':'data saved successfully','username':usr.username},status=200,content_type='application/json')
            else:
                return JsonResponse({'valid':False,'uform_errors':form.errors},status=200,content_type='application/json')


#WeAreGlad
def WeAreGlad(request):
    obj=check_data()
    if not obj:
        return redirect('/installation/')
    data={
        'title':'We are glad you joined us',
        'data':request.user,
        'obj':obj,
    }
    return render(request,'panel/glad.html',context=data)

#Home
@method_decorator(unauthenticated_user,name='dispatch')
class Home(View):
    def get(self,request):
        obj=check_data()
        if not obj:
            return redirect('/installation/')
        loginform=UserLoginForm()
        regform=UserReg()
        catform=ExtEmailReg()
        data={
            'title':'Login',
            'obj':obj,
            'data':request.user,
            'loginform':loginform,
            'regform':regform,
            'login':True,
            'catform':catform,
            'data':request.user,
        }
        return render(request,'panel/login.html',context=data)
    def post(self,request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            key=request.POST['username']
            password=request.POST['password']
            if key:
                if password:
                    regex=re.compile(r'([A-Za-z0-9+[.-_]])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z/a-z]{2,})+')
                    if re.fullmatch(regex,key):
                        #email address
                        if User.objects.filter(email=key).exists():
                            data=User.objects.get(email=key)
                            user=authenticate(username=data.username,password=password)
                        else:
                            uform_errors={"username": ["Invalid email address."]}
                            return JsonResponse({'valid':False,'uform_errors':uform_errors},content_type="application/json")
                    else:
                        #username
                        if User.objects.filter(username=key).exists():
                           user=authenticate(username=key,password=password)
                        else:
                            uform_errors={"username": ["Invalid username."]}
                            return JsonResponse({'valid':False,'uform_errors':uform_errors},content_type="application/json")
                        
                    if user is not None:
                        if 'rememberme' in request.POST:
                           request.session.set_expiry(1209600) #two weeeks
                        else:
                           request.session.set_expiry(0)
                        login(request,user)
                        return JsonResponse({'message':'success:Login Successfully.','login':True},content_type="application/json")
                    uform_errors={"password": ["Password is incorrect."]}
                    return JsonResponse({'valid':False,'uform_errors':uform_errors},content_type="application/json")
                else:
                    uform_errors={"password": ["Password is required."]}
                    return JsonResponse({'valid':False,'uform_errors':uform_errors},content_type="application/json")
            else:
                uform_errors={"username": ["Username/Email Address is required."]}
                return JsonResponse({'valid':False,'uform_errors':uform_errors},content_type="application/json")
   

#logout
def user_logout(request):
    logout(request)
    return redirect('/accounts/login/')       

def register(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form=UserReg(request.POST or None)
        form1=ExtEmailReg(request.POST or None)
        if form.is_valid() and form1.is_valid():
            userme=form.save(commit=False)
            userme.username=form.cleaned_data.get('email',None).split('@')[0]
            userme.is_active=True
            userme.save()
            if not Group.objects.filter(name=form1.cleaned_data.get('category',None)).exists():
                group=Group.objects.create(name=form1.cleaned_data.get('category',None))
                group.user_set.add(userme)
                group.save()
            else:
                group=Group.objects.get(name__icontains=form1.cleaned_data.get('category',None))
                group.user_set.add(userme)
                group.save()
            extended=form1.save(commit=False)
            extended.user=userme
            extended.temporary_password=form.cleaned_data.get('password1',None)
            extended.pending_verification=True
            extended.save()
            return JsonResponse({'message':'Registered successfuly.','register':True,'email':userme.email},content_type='application/json')
        else:
            return JsonResponse({'valid':False,'uform_errors':form.errors,'eform_errors':form1.errors},content_type='application/json')


#dashboard
@method_decorator(login_required(login_url='/accounts/login/'),name='dispatch')
class dashboard(View):
    def get(self,request):
        obj=check_data()
        if not obj:
            return redirect('/installation/')
        form=TweetForm()
        data={
                'title':'Dashboard',
                'obj':obj,
                'data':request.user,
                'form':form,
            }
        return render(request,'panel/dashboard.html',context=data)

    def post(self,request,*args ,**kwargs):
        form=TweetForm(request.POST,request.FILES or None)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.user=request.user
            obj.save()
            user=ExtendedAuthUser.objects.get(user_id=request.user.pk)
            user.tweets=int(user.tweets)+1
            user.save()
            if obj.tweet_image:
                image=obj.tweet_image
            else:
                image=''
            response={
                'user_id':request.user.pk,
                'username':request.user.username,
                'name':request.user.get_full_name(),
                'profile':request.user.extendedauthuser.profile_pic.url,
            }
            return JsonResponse({'tweet_id':obj.id,'image':image,'valid':True,'message':'Tweet posted successfully.','tweet':True,'response':response,'tweeted_message':obj.message},content_type='application/json')
        else:
            return JsonResponse({'valid':False,'uform_errors':form.errors},content_type='application/json')

#tweetForm
@method_decorator(login_required(login_url='/accounts/login/'),name='dispatch')
class tweetForm(View):
    def get(self,request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            obj=check_data()
            if not obj:
                return redirect('/installation/')
            form=TweetForm()
            data={
                    'title':'Tweet',
                    'obj':obj,
                    'data':request.user,
                    'form':form,
                }
            return render(request,'panel/tweetform.html',context=data)
        return HttpResponse('Method not allowed')
    def post(self,request,*args ,**kwargs):
        form=TweetForm(request.POST,request.FILES or None)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.user=request.user
            obj.save()
            return JsonResponse({'valid':True,'message':'Tweet posted successfully.','tweet':True},content_type='application/json')
        else:
            return JsonResponse({'valid':False,'uform_errors':form.errors},content_type='application/json')


#commentForm
@method_decorator(login_required(login_url='/accounts/login/'),name='dispatch')
class commentForm(View):
    def get(self,request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            obj=check_data()
            if not obj:
                return redirect('/installation/')
            comment_id=request.GET.get('showpopup')
            tweet=get_object_or_404(TweetModel,id__exact=comment_id)
            results=CommentModel.objects.filter(parent_id__exact=comment_id).order_by("-id")
            paginator=Paginator(results,30)
            page_num=request.GET.get('page',1)
            try:
                comments=paginator.page(page_num)
            except PageNotAnInteger:
                comments=paginator.page(1)
            except EmptyPage:
                comments=paginator.page(paginator.num_pages)
            data={
                    'title':'Comment',
                    'obj':obj,
                    'data':request.user,
                    'tweet':tweet,
                    'comments':comments,
                    'comments_count':paginator.count,
                }
            return render(request,'panel/commentform.html',context=data)
        return HttpResponse('Method not allowed')
    def post(self,request,*args ,**kwargs):
        form=CommentForm(request.POST or None)
        if form.is_valid():
            comment_id=request.POST.get('comment_id')
            obj=form.save(commit=False)
            obj.user=request.user
            tweet=get_object_or_404(TweetModel,id__exact=comment_id)
            obj.parent=tweet
            obj.save()

            results=CommentModel.objects.filter(parent_id__exact=comment_id).order_by("-id")
            paginator=Paginator(results,30)
            page_num=request.GET.get('page',1)
            try:
                comments=paginator.page(page_num)
            except PageNotAnInteger:
                comments=paginator.page(1)
            except EmptyPage:
                comments=paginator.page(paginator.num_pages)
            tweet.comment_count=paginator.count
            tweet.save()
            ActivityModel.objects.update_or_create(sender=request.user,receiver=tweet.user.id,message=f'{request.user.username} commented on your tweet',defaults={'message':f'{request.user.username} commented on your tweet'})
            serializer=CommentSerializers(comments,many=True)
            response={
                'user_id':request.user.pk,
                'username':request.user.username,
                'name':request.user.get_full_name(),
                'profile':request.user.extendedauthuser.profile_pic.url,
                'comments_count':intcomma(paginator.count),
            }
            return JsonResponse({'comment':True,'data':serializer.data,'response':response,'message':'Comment posted successfully.'},content_type='application/json')
        else:
            return JsonResponse({'valid':False,'uform_errors':form.errors},content_type='application/json')


#retrieveChatForm
@login_required(login_url='/accounts/login/')
def retrieveChatForm(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        obj=check_data()
        form=ChatForm()
        user_id=request.GET.get('user_id')
        print('user_id:',user_id)
        messages=ChatModel.objects.filter(sender=request.user.pk,receiver=user_id) | ChatModel.objects.filter(receiver=request.user.pk,sender=user_id)
        data={
                'title':'ChatForm',
                'obj':obj,
                'data':request.user,
                'messages':messages,
                'form':form,
            }
        return render(request,'panel/chatform.html',context=data)
    return HttpResponse('Method not allowed')



#postRetweet
@method_decorator(login_required(login_url='/accounts/login/'),name='dispatch')
class postRetweet(View):
    def get(self,request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            obj=check_data()
            if not obj:
                return redirect('/installation/')
            tweet_id=request.GET.get('showPopup')
            tweet=get_object_or_404(TweetModel,id__exact=tweet_id)
            data={
                    'title':'Post Retweet',
                    'obj':obj,
                    'data':request.user,
                    'tweet':tweet,
                }
            return render(request,'panel/retweet_form.html',context=data)
        return HttpResponse('Method not allowed')
    def post(self,request,*args ,**kwargs):
        form=RetweetForm(request.POST or None)
        if form.is_valid():
            tweet_id=request.POST.get('tweet_id')
            tweet=get_object_or_404(TweetModel,id__exact=tweet_id)
            obj=form.save(commit=False)
            obj.user=request.user
            obj.message=tweet.message
            obj.retweeted_by=request.user.username
            obj.is_retweet=True
            obj.retweeted_id=tweet_id
            obj.save()
            count=TweetModel.objects.filter(is_retweet=True,retweeted_id=tweet_id).count()
            twit=TweetModel.objects.get(id__exact=tweet_id)
            twit.retweet_count=count
            twit.save()
            ActivityModel.objects.update_or_create(sender=request.user,receiver=tweet.user.id,message=f'{request.user.username} retweeted your tweet',defaults={'message':f'{request.user.username} retweeted your tweet'})
            return JsonResponse({'retweeted':True,'message':'Tweet retweeted successfully.'},content_type='application/json')
        else:
            return JsonResponse({'valid':False,'uform_errors':form.errors},content_type='application/json')

#accountMessages
@method_decorator(login_required(login_url='/accounts/login/'),name='dispatch')
class accountMessages(View):
    def get(self,request):
        obj=check_data()
        if not obj:
            return redirect('/installation/')


        if ChatModel.objects.filter(receiver=request.user.pk,is_read=False).exists():
            last_message=ChatModel.objects.filter(receiver=request.user.pk,is_read=False).last()
            if last_message.receiver ==request.user.pk:
                is_receiver=True
            else:
                is_receiver=False
        else:
            is_receiver=False

        inner_qs=ChatModel.objects.filter(sender_id=request.user.pk).values_list('receiver',flat=True).distinct()
        results=User.objects.exclude(id=request.user.pk).exclude(id__in=inner_qs).order_by("-id")
        paginator=Paginator(results,30)
        page_num=request.GET.get('page')
        contacts=paginator.get_page(page_num)

        chats_results=User.objects.filter(id__in=inner_qs).order_by("-id")
        paginator1=Paginator(chats_results,30)
        page_num1=request.GET.get('page')
        chats=paginator1.get_page(page_num1)
        data={
                'title':'Account Messages',
                'obj':obj,
                'data':request.user,
                'messages':True,
                'contacts':contacts,
                'chats':chats,
                'is_receiver':is_receiver,
            }
        return render(request,'panel/messages.html',context=data)
       

#settings
@method_decorator(login_required(login_url='/accounts/login/'),name='dispatch')
class Settings(View):
    def get(self,request):
        obj=check_data()
        if not obj:
            return redirect('/installation/')
        form=CurrentStaffLoggedInUserProfileChangeForm(instance=request.user)
        passform=UserPasswordChangeForm()
        data={
                'title':'Settings',
                'obj':obj,
                'data':request.user,
                'form':form,
                'passform':passform,
            }
        return render(request,'panel/settings.html',context=data)
    def post(self,request,*args ,**kwargs):
        form=CurrentStaffLoggedInUserProfileChangeForm(request.POST or None,instance=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({'valid':True,'message':'Profile updated successfully.'},content_type='application/json')
        else:
            return JsonResponse({'valid':False,'uform_errors':form.errors},content_type='application/json')

#addTweet
@login_required(login_url='/accounts/login/')
@api_view(['POST',])
def addTweet(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        passform=UserPasswordChangeForm(request.POST or None,instance=request.user)
        if passform.is_valid():
            user=User.objects.get(username__exact=request.user.username)
            user.password=make_password(passform.cleaned_data.get('password1'))
            user.save()
            update_session_auth_hash(request,request.user)
            return JsonResponse({'valid':True,'message':'Password changed successfully.'},content_type='application/json')
        else:
            return JsonResponse({'valid':False,'uform_errors':passform.errors},content_type='application/json')

#notifications
@login_required(login_url='/accounts/login/')
@api_view(['GET',])
def notifications(request):
    obj=check_data()
    if not obj:
        return redirect('/installation/')
    notifications=ActivityModel.objects.filter(receiver=request.user.pk,is_read=False)
    for notification in notifications:
        notification.is_read=True
        notification.save()
    data={
            'title':'Notifications',
            'obj':obj,
            'data':request.user,
        }
    return render(request,'panel/notification.html',context=data)


#chatroom
@login_required(login_url='/accounts/login/')
@api_view(['GET',])
def chatroom(request):
    obj=check_data()
    if not obj:
        return redirect('/installation/')
    form=ChatForm()
    messages=ChatModel.objects.filter(sender=request.user.pk) | ChatModel.objects.filter(receiver=request.user.pk)
    inner_qs=ChatModel.objects.exclude(sender_id=request.user.pk).values_list('sender_id',flat=True).distinct()
    results=User.objects.exclude(id=request.user.pk).exclude(chatmodel__sender_id__in=inner_qs).order_by("-id")
    paginator=Paginator(results,30)
    page_num=request.GET.get('page')
    users=paginator.get_page(page_num)

    chats_results=User.objects.filter(id__in=inner_qs).order_by("-id")
    paginator1=Paginator(chats_results,30)
    page_num1=request.GET.get('page')
    chats=paginator1.get_page(page_num1)
    data={
            'title':'Dashboard',
            'obj':obj,
            'data':request.user,
            'login':True,
            'room-name':request.user.username,
            'form':form,
            'users':users,
            'messages':messages,
            'chats':chats,
            'users_count':paginator.count,
        }
    return render(request,'panel/chat.html',context=data)


@login_required(login_url='/accounts/login/')
@api_view(['GET',])
def profileView(request,username):
    obj=check_data()
    if not obj:
        return redirect('/installation/')
    user = get_object_or_404(User,username=username)
    form=CurrentStaffLoggedInUserProfileChangeForm(instance=user)
    eform=CurrentAdminExtUserProfileChangeForm(instance=user.extendedauthuser)
    passform=UserPasswordChangeForm()
    profileform=ProfilePicForm()
    actionform=ActionForm(instance=user.extendedauthuser)
    results=TweetModel.objects.filter(user_id=user.id).order_by("-id")
    paginator=Paginator(results,10)
    page_num=request.GET.get('page',1)
    try:
        tweets=paginator.page(page_num)
    except PageNotAnInteger:
        tweets=paginator.page(1)
    except EmptyPage:
        tweets=paginator.page(paginator.num_pages)

    data={
        'title':f'Profile / {user.username}',
        'obj':obj,
        'data':user,
        'form':form,
        'eform':eform,
        'passform':passform,
        'profileform':profileform,
        'actionform':actionform,
        'room_name':request.user.username,
        'tweets':tweets,
        'tweets_count':paginator.count,
    }
    return render(request,'panel/profile.html',context=data)
 


#EditrofileView
@method_decorator(login_required(login_url='/accounts/login/'),name='dispatch')
class EditrofileView(View):
    def get(self,request,username):
        obj=check_data()
        if not obj:
            return redirect('/installation/')
        user = get_object_or_404(User,username=username)
        form=CurrentStaffLoggedInUserProfileChangeForm(instance=user)
        eform=CurrentAdminExtUserProfileChangeForm(instance=user.extendedauthuser)
        passform=UserPasswordChangeForm()
        profileform=ProfilePicForm()
        actionform=ActionForm(instance=user.extendedauthuser)
        data={
            'title':f'Edit profile / {user.username}',
            'obj':obj,
            'data':request.user,
            'form':form,
            'eform':eform,
            'passform':passform,
            'profileform':profileform,
            'actionform':actionform,
            'room_name':request.user.username,
        }
        return render(request,'panel/edit.html',context=data)
 
    def post(self,request,username,*args ,**kwargs):
        form=CurrentStaffLoggedInUserProfileChangeForm(request.POST or None,instance=request.user)
        eform=CurrentAdminExtUserProfileChangeForm(request.POST,request.FILES or None, instance=request.user.extendedauthuser)
        if form.is_valid() and eform.is_valid():
            form.save()
            eform.save()
            return JsonResponse({'valid':True,'message':'Profile updated successfully.','profile_pic':True},content_type='application/json')
        else:
            return JsonResponse({'valid':False,'uform_errors':form.errors,'eform_errors':eform.errors,},content_type='application/json')

#profilePic
@login_required(login_url='/accounts/login/')
@api_view(['POST',])
def profilePic(request):
    if request.method == 'POST':
        profilePicform=ProfilePicForm(request.POST , request.FILES or None , instance=request.user.extendedauthuser)
        if profilePicform.has_changed():
            if profilePicform.is_valid():
                userme=profilePicform.save(commit=False)
                userme.user=request.user
                userme.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                return JsonResponse({'valid':False,'uform_errors':profilePicform.errors},status=200)    
        return JsonResponse({'valid':False,'error':'No changes made'},content_type='application/json')


#coverPic
@login_required(login_url='/accounts/login/')
@api_view(['POST',])
def coverPic(request):
    if request.method == 'POST':
        profilePicform=ProfilePicForm(request.POST , request.FILES or None , instance=request.user.extendedauthuser)
        if profilePicform.has_changed():
            if profilePicform.is_valid():
                userme=profilePicform.save(commit=False)
                userme.user=request.user
                userme.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                return JsonResponse({'valid':False,'uform_errors':profilePicform.errors},status=200)    
        return JsonResponse({'valid':False,'error':'No changes made'},content_type='application/json')

#removeProfilePic
@login_required(login_url='/accounts/login/')
@api_view(['GET',])
def removeProfilePic(request):
    if request.method == 'GET':
        user=ExtendedAuthUser.objects.get(user_id__exact=request.user.pk)
        user.profile_pic='placeholder.png'
        user.save()
        return redirect(request.META['HTTP_REFERER'])


#removeCoverPic
@login_required(login_url='/accounts/login/')
@api_view(['GET',])
def removeCoverPic(request):
    if request.method == 'GET':
        user=ExtendedAuthUser.objects.get(user_id__exact=request.user.pk)
        user.cover_pic='cover.png'
        user.save()
        return redirect(request.META['HTTP_REFERER'])

#passwordChange
@login_required(login_url='/accounts/login/')
@api_view(['POST',])
def passwordChange(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        passform=UserPasswordChangeForm(request.POST or None,instance=request.user)
        if passform.is_valid():
            user=User.objects.get(username__exact=request.user.username)
            user.password=make_password(passform.cleaned_data.get('password1'))
            user.save()
            update_session_auth_hash(request,request.user)
            return JsonResponse({'valid':True,'message':'Password changed successfully.'},content_type='application/json')
        else:
            return JsonResponse({'valid':False,'uform_errors':passform.errors},content_type='application/json')



#postLike
@csrf_exempt
@login_required(login_url='/accounts/login/')
def postLike(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        id=request.POST.get('like',None)
        post=get_object_or_404(TweetModel,id__exact=id)
        if  post.likes_count is None:
            post.likes_count=1
        else:
            post.likes_count=int(post.likes_count)+1
        post.save()
        LikeModel.objects.update_or_create(parent_id=id,user=request.user,defaults={'liked':True})
        ActivityModel.objects.update_or_create(sender=request.user,receiver=post.user_id,message=f'{request.user.username} liked your tweet',defaults={'message':f'{request.user.username} liked your tweet'})
        return JsonResponse({'liked':True,'message':'Post liked!'},content_type='application/json')



#commentLike
@csrf_exempt
@login_required(login_url='/accounts/login/')
def commentLike(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        id=request.POST.get('like',None)
        comment=get_object_or_404(CommentModel,id__exact=id)
        comment.likes_count=int(comment.likes_count)+1
        comment.save()
        CommentLikeModel.objects.update_or_create(parent_id=id,user=request.user,defaults={'liked':True})
        return JsonResponse({'liked':True,'message':'Comment liked!'},content_type='application/json')


#commentUnlike
@csrf_exempt
@login_required(login_url='/accounts/login/')
def commentUnlike(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        id=request.POST.get('unlike',None)
        comment=get_object_or_404(CommentModel,id__exact=id)
        comment.likes_count=int(comment.likes_count)-1
        comment.save()
        CommentLikeModel.objects.update_or_create(parent_id=id,user=request.user,defaults={'liked':True})
        return JsonResponse({'liked':False,'message':'Comment unliked!'},content_type='application/json')

#postUnlike
@csrf_exempt
@login_required(login_url='/accounts/login/')
def postUnlike(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        id=request.POST.get('unlike',None)
        post=get_object_or_404(TweetModel,id__exact=id)
        if  post.likes_count is None:
            post.likes_count=0
        else:
            post.likes_count=int(post.likes_count)-1
        post.save()
        LikeModel.objects.update_or_create(parent_id=id,user=request.user,defaults={'liked':False})
        return JsonResponse({'liked':False,'message':'Post unliked!'},content_type='application/json')




#postComment
@csrf_exempt
@login_required(login_url='/accounts/login/')
def postComment(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        print('post:',request.POST)

#actionForm
@login_required(login_url='/accounts/login/')
@api_view(['POST',])
def actionForm(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        actionform=ActionForm(request.POST or None,instance=request.user.extendedauthuser)
        if actionform.is_valid():
            actionform.save()
            return JsonResponse({'valid':True,'message':'Changes saved successfully.'},content_type='application/json')
        else:
            return JsonResponse({'valid':False,'uform_errors':actionform.errors},content_type='application/json')


#EditSite
@method_decorator(login_required(login_url='/accounts/login/'),name='dispatch')
@method_decorator(allowed_users(allowed_roles=['admins']),name='dispatch')
class EditSite(View):
    def get(self,request):
        obj=check_data()
        form1=SiteForm(instance=obj)
        form2=AddressConfigForm(instance=obj)
        form3=SiteSocialForm(instance=obj)
        form4=WorkingConfigForm(instance=obj)
        data={
            'title':'Edit Site Settings',
            'obj':obj,
            'data':request.user,
            'form1':form1,
            'form2':form2,
            'form3':form3,
            'form4':form4,
            'room_name':request.user.username,
        }
        return render(request,'panel/site.html',context=data)
    def post(self,request,*args , **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            instance_data=SiteModel.objects.all().first()
            form=SiteForm(request.POST,request.FILES or None , instance=instance_data)
            if form.is_valid():
                form.save()
                return JsonResponse({'valid':True,'message':'data saved successfully'},status=200,content_type='application/json')
            else:
                return JsonResponse({'valid':False,'uform_errors':form.errors},status=200,content_type='application/json')

#siteWorking
@login_required(login_url='/accounts/login/')
@allowed_users(allowed_roles=['admins'])
@api_view(['POST',])
def siteWorking(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        instance_data=SiteModel.objects.all().first()
        form=WorkingConfigForm(request.POST, request.FILES or None , instance=instance_data)
        if form.is_valid():
            form.save()
            return JsonResponse({'valid':True,'message':'data saved successfully'},status=200,content_type='application/json')
        else:
            return JsonResponse({'valid':False,'uform_errors':form.errors},status=200,content_type='application/json')

#siteContact
@login_required(login_url='/accounts/login/')
@allowed_users(allowed_roles=['admins'])
@api_view(['POST',])
def siteContact(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        instance_data=SiteModel.objects.all().first()
        form=AddressConfigForm(request.POST or None , instance=instance_data)
        if form.is_valid():
            form.save()
            return JsonResponse({'valid':True,'message':'data saved successfully'},status=200,content_type='application/json')
        else:
            return JsonResponse({'valid':False,'uform_errors':form.errors},status=200,content_type='application/json')


#siteSocial
@login_required(login_url='/accounts/login/')
@allowed_users(allowed_roles=['admins'])
@api_view(['POST',])
def siteSocial(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        instance_data=SiteModel.objects.all().first()
        form=SiteSocialForm(request.POST or None , instance=instance_data)
        if form.is_valid():
            link=form.save(commit=False)
            link.facebook=request.POST['facebook']
            link.twitter=request.POST['twitter']
            link.instagram=request.POST['instagram']
            link.linkedin=request.POST['linkedin']
            link.whatsapp=request.POST['whatsapp']
            link.youtube=request.POST['youtube']
            link.save()
            return JsonResponse({'valid':True,'message':'data saved successfully'},status=200,content_type='application/json')
        else:
 

            return JsonResponse({'valid':False,'uform_errors':form.errors},status=200,content_type='application/json')


@login_required(login_url='/accounts/login/')
@api_view(['POST',])
def chat(request,id):
   if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form=ChatForm(request.POST or None)
        if form.is_valid():
            obj=form.save(commit=False)
            if ChatModel.objects.filter(id__isnull=False):
                chat=ChatModel.objects.all().last()
                if chat.receiver == request.user.pk:
                    updates=ChatModel.objects.filter(receiver=request.user.pk,is_read=False)
                    for item in updates:
                        item.is_read=True  
                        item.save()
                    obj.sender=request.user
                    obj.receiver=id
                else:
                    obj.sender=request.user
                    obj.receiver=id
            else:
                obj.sender=request.user
                obj.receiver=id
            obj.save()
            messages_count=ChatModel.objects.filter(receiver=id,is_read=False).count()

            user=ExtendedAuthUser.objects.get(user_id__exact=request.user.pk)
            user.unread_messages=messages_count
            user.single_message=form.cleaned_data.get('message',None)
            user.receiver=id
            user.save()
            response={
                        'chat':True,
                        'new_message':'Message sent!',
                        'submitted_message':form.cleaned_data.get('message',None),
                        'time':'just now',
                        'current_username':request.user.username,
                        'name':request.user.get_full_name(),
                    }
            return JsonResponse(response,content_type='application/json')
        return JsonResponse({'valid':False,'uform_errors':form.errors},content_type='application/json')

#updateStatus
@login_required(login_url='/accounts/login')
@api_view(['GET',])
def updateStatus(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user=ExtendedAuthUser.objects.get(user_id=request.user.pk)
        status=request.GET.get('status',None)
        if status:
            user.is_online=True
        else:
            user.is_online=False
        user.save()
        return JsonResponse({'online':True,'message':'Connected.'},content_type='application/json')




#userFollow
@login_required(login_url='/accounts/login')
@api_view(['GET',])
def userFollow(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        follow_id=request.GET.get('follow',None)
        FollowModel.objects.update_or_create(sender=request.user,receiver=follow_id,defaults={'receiver':follow_id})
        follow_count=FollowModel.objects.filter(sender_id=request.user.pk).count()
        user=ExtendedAuthUser.objects.get(user_id=request.user.pk)
        user.following=follow_count
        user.save()
        user1=ExtendedAuthUser.objects.get(user_id=follow_id)
        user1.followers=int(user1.followers)+1
        user1.save()
        ActivityModel.objects.update_or_create(sender=request.user,receiver=follow_id,message=f'{request.user.username} followed you.',defaults={'message':f'{request.user.username} followed you.'})
        return JsonResponse({'follow':True,'message':f'Following ({intcomma(follow_count)})','following':follow_count},content_type='application/json')



#userUnfollow
@login_required(login_url='/accounts/login')
@api_view(['GET',])
def userUnfollow(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        unfollow_id=request.GET.get('unfollow',None)
        follow=FollowModel.objects.filter(sender_id=request.user,receiver=unfollow_id)
        follow.delete()
        follow_count=FollowModel.objects.filter(sender_id=request.user.pk).count()
        user=ExtendedAuthUser.objects.get(user_id=request.user.pk)
        user.following=follow_count
        user.save()
        user1=ExtendedAuthUser.objects.get(user_id=unfollow_id)
        user1.followers=int(user1.followers)-1
        user1.save()
        return JsonResponse({'follow':True,'message':f'Following ({intcomma(follow_count)})','following':follow_count},content_type='application/json')


#accountUsers
@login_required(login_url='/accounts/login/')
@api_view(['GET',])
def accountUsers(request):
    obj=check_data()
    if not obj:
        return redirect('/installation/')
    inner_qs=FollowModel.objects.values_list('receiver',flat=True).distinct()
    user_results=User.objects.exclude(is_superuser=True).exclude(id__in=inner_qs).order_by("-id")
    paginator1=Paginator(user_results,30)
    page_num1=request.GET.get('page',1)
    try:
        users=paginator1.page(page_num1)
    except PageNotAnInteger:
        users=paginator1.page(1)
    except EmptyPage:
        users=paginator1.page(paginator1.num_pages)
    data={
        'title':'Users',
        'obj':obj,
        'data':request.user,
        'room_name':request.user.username,
        'users':users
    }
    return render(request,'panel/users.html',context=data)


#accountFollowers
@login_required(login_url='/accounts/login/')
@api_view(['GET',])
def accountFollowers(request,username):
    obj=check_data()
    if not obj:
        return redirect('/installation/')
    inner_qs=FollowModel.objects.values_list('receiver',flat=True).distinct()
    user_results=User.objects.filter(id__in=inner_qs).order_by("-id")
    paginator1=Paginator(user_results,30)
    page_num1=request.GET.get('page',1)
    try:
        users=paginator1.page(page_num1)
    except PageNotAnInteger:
        users=paginator1.page(1)
    except EmptyPage:
        users=paginator1.page(paginator1.num_pages)
    data={
        'title':f'Your followers ({intcomma(paginator1.count)})',
        'obj':obj,
        'data':request.user,
        'room_name':request.user.username,
        'follows':users,
        'followers':True,
    }
    return render(request,'panel/users.html',context=data)


#accountFollowing
@login_required(login_url='/accounts/login/')
@api_view(['GET',])
def accountFollowing(request,username):
    obj=check_data()
    if not obj:
        return redirect('/installation/')
    inner_qs=FollowModel.objects.filter(sender_id=request.user.pk).values_list('receiver',flat=True).distinct()
    user_results=User.objects.filter(id__in=inner_qs).order_by("-id")
    paginator1=Paginator(user_results,30)
    page_num1=request.GET.get('page',1)
    try:
        users=paginator1.page(page_num1)
    except PageNotAnInteger:
        users=paginator1.page(1)
    except EmptyPage:
        users=paginator1.page(paginator1.num_pages)
    data={
        'title':f'Following ({intcomma(paginator1.count)})',
        'obj':obj,
        'data':request.user,
        'room_name':request.user.username,
        'follows':users,
        'following':True,
    }
    return render(request,'panel/users.html',context=data)


#deleteTweet
@login_required(login_url='/accounts/login')
def deleteTweet(request,id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        tweet=get_object_or_404(TweetModel,id__exact=id)
        tweet.delete()
        return JsonResponse({'deleted':True,'message':'Tweet deleted!'},content_type='application/json')


#deleteComment
@login_required(login_url='/accounts/login')
def deleteComment(request,id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        comment=get_object_or_404(CommentModel,id__exact=id)
        comment.delete()
        count=CommentModel.objects.filter(parent_id__exact=comment.parent_id).count()
        return JsonResponse({'deleted':True,'message':'Comment deleted!','comment_count':count},content_type='application/json')

#userSearch
@login_required(login_url='/accounts/login')
def userSearch(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        results=searchUser(request.GET.get('search',None))
        if results:
            serializer=UserSerlializer(results,many=True)
            return JsonResponse({'search':True,'results':serializer.data},content_type='application/json')
        else:
            return JsonResponse({'search':False,'results':None},content_type='application/json')

#searchChat
@login_required(login_url='/accounts/login')
def searchChat(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        results=searchUser(request.GET.get('search',None))
        if results:
            serializer=UserSerlializer(results,many=True)
            return JsonResponse({'search':True,'results':serializer.data},content_type='application/json')
        else:
            return JsonResponse({'search':False,'results':None},content_type='application/json')


#retrieveChats
@login_required(login_url='/accounts/login')
def retrieveChats(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        id=request.GET.get('user_id',None)#
        user=get_object_or_404(User,id__exact=id)
        obj=check_data()
        messages=ChatModel.objects.filter(sender=request.user.pk,receiver=id) | ChatModel.objects.filter(receiver=request.user.pk,sender=id)
        messages=ChatModel.objects.filter(receiver=request.user.pk,is_read=False)
        for message in messages:
            message.is_read=True
            message.save()
        form=ChatForm()
        data={
                'title':'Account Messages',
                'obj':obj,
                'data':request.user,
                'form':form,
                'my_messages':messages,
                'user':user,
            }
        return render(request,'panel/new_chat.html',context=data)


#searchForm
@login_required(login_url='/accounts/login')
def searchForm(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        obj=check_data()
        search=request.GET.get('search',None)
        results=searchUser(request.GET.get('search',None))
        data={
                'title':'Search Form',
                'obj':obj,
                'data':request.user,
                'search':search,
                'results':results,
            }
        return render(request,'panel/search_form.html',context=data)