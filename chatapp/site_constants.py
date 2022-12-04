import environ
from django.conf import settings
from panel.models import *
from django.contrib.auth.forms import User
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
env=environ.Env()
environ.Env().read_env()


def export_vars(request):
    results=TweetModel.objects.prefetch_related('likemodel_set').all().order_by("-id")
    paginator=Paginator(results,8)
    page_num=request.GET.get('page',1)
    try:
        tweets=paginator.page(page_num)
    except PageNotAnInteger:
        tweets=paginator.page(1)
    except EmptyPage:
        tweets=paginator.page(paginator.num_pages)


    inner_qs=FollowModel.objects.filter(sender=request.user.pk).values_list('receiver',flat=True).distinct()
    user_results=User.objects.exclude(id=request.user.pk).exclude(id__in=inner_qs).order_by("-id")
    paginator1=Paginator(user_results,10)
    page_num1=request.GET.get('page',1)
    try:
        users=paginator1.page(page_num1)
    except PageNotAnInteger:
        users=paginator1.page(1)
    except EmptyPage:
        users=paginator1.page(paginator1.num_pages)


    notifications_count=ActivityModel.objects.filter(receiver=request.user.pk,is_read=False).count()
    page_results=ActivityModel.objects.filter(receiver=request.user.pk).order_by("-id")
    paginator2=Paginator(page_results,10)
    page_num2=request.GET.get('page',1)
    try:
        notifications=paginator2.page(page_num2)
    except PageNotAnInteger:
        notifications=paginator2.page(1)
    except EmptyPage:
        notifications=paginator2.page(paginator2.num_pages)
    chat_count=ChatModel.objects.filter(receiver=request.user.pk,is_read=False).count()
    data={
            'site_name':env('SITE_NAME'),
            'site_url':env('SITE_URL'),
     	    'designer_link':env('SITE_DESIGNER_LINK'),
            'designer_name':env('SITE_DESIGNER_NAME'),
            'designer portfolio':env('SITE_DESIGNER_NAME'),
            'facebook_link':env('FACEBOOK_LINK'),
            'twitter_link':env('TWITTER_LINK'),
            'instagram_link':env('INSTAGRAM_LINK'),
            'whatsapp_link':env('WHATSAPP_LINK'),
            'linkedin_link':env('LINKEDIN_LINK'),
            'tweets':tweets,
            'user_followers':users,
            'room_name':request.user.username,
            'users_count':paginator1.count,
            'notifications':notifications,
            'notifications_count':notifications_count,
            'chat_count':chat_count,
    }
    return data