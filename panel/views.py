from django.shortcuts import render
from django.http import JsonResponse,HttpResponse,HttpResponseBadRequest
from django.shortcuts import render,get_object_or_404,redirect
from asgiref.sync import sync_to_async
from installation.models import SiteModel
import time,asyncio
from django.core.paginator import Paginator
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
from channels.layers import get_channel_layer
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password
from django.db.models import Avg
import timeago,datetime
from  django.contrib.auth.models import Group
from datetime import timedelta
import PyPDF2
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
            extended.pending_verification=True
            extended.save()
            user=authenticate(username=userme.username,password=form.cleaned_data.get('password1',None))
            if user is not None:
                login(request,user)
            return JsonResponse({'message':'Registered successfuly.','register':True},content_type='application/json')
        else:
            return JsonResponse({'valid':False,'uform_errors':form.errors,'eform_errors':form1.errors},content_type='application/json')

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


#ProfileView
@method_decorator(login_required(login_url='/accounts/login/'),name='dispatch')
class ProfileView(View):
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
        return render(request,'panel/profile.html',context=data)
 
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
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        profilePicform=ProfilePicForm(request.POST , request.FILES or None , instance=request.user.extendedauthuser)
        if profilePicform.has_changed():
            if profilePicform.is_valid():
                userme=profilePicform.save(commit=False)
                userme.user=request.user
                userme.save()
                return JsonResponse({'valid':True,'message':'Profile picture updated.'},status=200,safe=False)
            else:
                return JsonResponse({'valid':False,'uform_errors':profilePicform.errors},status=200)    
        return JsonResponse({'valid':False,'error':'No changes made'},content_type='application/json')


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
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
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
                        'valid':True,
                        'new_message':'Message sent!',
                        'submitted_message':form.cleaned_data.get('message',None),
                        'time':'just now',
                        'profiler':request.user.extendedauthuser.profile_pic.url,
                        'name':request.user.username,
                    }
            return JsonResponse(response,content_type='application/json')
        return JsonResponse({'valid':False,'uform_errors':form.errors},content_type='application/json')

#updateStatus
@csrf_exempt
@login_required(login_url='/accounts/login')
@api_view(['GET',])
def updateStatus(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user=ExtendedAuthUser.objects.get(user_id=request.user.pk)
        status=request.POST.get('status',None)
        if status:
            user.is_online=True
        else:
            user.is_online=False
        user.save()
        return JsonResponse({'saved':True,'message':'data saved.'},content_type='application/json')