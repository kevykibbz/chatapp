from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .utils import send_email
import random
from installation.models import SiteModel
from .tokens import create_token
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import jsonfield
from channels.layers import get_channel_layer
import json
from asgiref.sync import async_to_sync
from ckeditor_uploader.fields import RichTextUploadingField
from installation.models import SiteModel
from django.utils.crypto import get_random_string
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Max
from django.utils.translation import gettext_lazy as _
import environ
from django.contrib.humanize.templatetags.humanize import intcomma,naturaltime
import timeago,datetime
env=environ.Env()
environ.Env.read_env()

     
#generate random
def generate_id():
    return get_random_string(6,'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKMNOPQRSTUVWXYZ0123456789')


#generate random
def generate_serial():
    return get_random_string(12,'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKMNOPQRSTUVWXYZ0123456789')


@receiver(post_save, sender=SiteModel)
def send_installation_email(sender, instance, created, **kwargs):
    if created:
        if instance.is_installed:
            #site is installed
            obj=SiteModel.objects.all()[0]
            subject='Congragulations:Site installed successfully.'
            email=instance.user.email
            message={
                        'user':instance.user,
                        'site_name':instance.site_name,
                        'site_url':instance.site_url,
                        'address':instance.address,
                        'location':instance.location,
                        'description':obj.description,
                        'phone':obj.phone
                     } 
            template='emails/installation.html'
            send_email(subject,email,message,template)





def bgcolor():
    hex_digits=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    digit_array=[]
    for i in range(6):
        digits=hex_digits[random.randint(0,15)]
        digit_array.append(digits)
    joined_digits=''.join(digit_array)
    color='#'+joined_digits
    return color





options=[
            ('---Select gender---',
                    (
                        ('Male','Male'),
                        ('Female','Female'),
                        ('Other','Other'),
                    )
            ),
        ]
class ExtendedAuthUser(models.Model):
    user=models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)
    phone=PhoneNumberField(null=True,blank=True,verbose_name='phone',unique=True,max_length=13)
    initials=models.CharField(max_length=10,blank=True,null=True)
    serial_no=models.CharField(max_length=100,default=get_random_string,null=True,blank=True)
    bgcolor=models.CharField(max_length=10,blank=True,null=True,default=bgcolor)
    company=models.CharField(max_length=100,null=True,blank=True,default=env('SITE_NAME'))
    zipcode=models.CharField(max_length=100,null=True,blank=True,default='416')
    city=models.CharField(max_length=100,null=True,blank=True,default='Nairobi')
    country=models.CharField(max_length=100,null=True,blank=True,default='Kenya')
    timezone=models.CharField(max_length=200,null=True,blank=True,default='Africa/Nairobi')
    profile_pic=models.ImageField(upload_to='profiles/',null=True,blank=True,default="placeholder.jpg")
    role=models.CharField(max_length=200,null=True,blank=True)
    unread_messages=models.IntegerField(blank=True,null=True)
    receiver=models.IntegerField(blank=True,null=True)
    single_message=models.TextField(null=True,blank=True)
    is_deactivated=models.BooleanField(default=False,blank=True,null=True)
    are_you_married=models.BooleanField(default=False,blank=True,null=True)
    are_you_available_for_chat=models.BooleanField(default=False,blank=True,null=True)
    are_you_working=models.BooleanField(default=False,blank=True,null=True)
    are_you_athletic=models.BooleanField(default=False,blank=True,null=True)
    are_you_studying=models.BooleanField(default=False,blank=True,null=True)
    pending_verification=models.BooleanField(default=False,blank=True,null=True)
    is_online=models.BooleanField(default=False,blank=True,null=True)
    bio=models.TextField(null=True,blank=True,default='something about you...')
    nickname=models.CharField(max_length=100,null=True,blank=True,default='Your nickname')
    facebook=models.CharField(max_length=200,null=True,blank=True,default='https://facebook.com/username')
    twitter=models.CharField(max_length=200,null=True,blank=True,default='https://twitter.com/username')
    instagram=models.CharField(max_length=200,null=True,blank=True,default='https://instagram.com/username')
    linkedin=models.CharField(max_length=200,null=True,blank=True,default='https://linkedin.com/username')
    gender=models.CharField(choices=options,max_length=6,null=True,blank=True)
    birthday=models.DateField(null=True,blank=True)
    updated_on=models.DateTimeField(auto_now=True)
    created_on=models.DateTimeField(default=now)
    class Meta:
        db_table='extended_auth_user'
        verbose_name_plural='extended_auth_users'
    def __str__(self)->str:
        return f'{self.user.username} extended auth profile'

    def delete(self, using=None,keep_parents=False):
        if self.essay or self.profile_pic or self.certificate:
            self.essay.storage.delete(self.essay.name)
            self.profile_pic.storage.delete(self.profile_pic.name)
            self.certificate.storage.delete(self.certificate.name)
        super().delete()


        
@receiver(post_save, sender=ExtendedAuthUser)
def send_success_email(sender, instance, created, **kwargs):
    if created and not instance.user.is_staff:
        #site is installed
        subject='Congragulations:Registration Successfully.'
        email=instance.user.email
        obj=SiteModel.objects.all()[0]
        message={
                    'user':instance.user,
                    'email':instance.user.email,
                    'address':obj.address,
                    'location':obj.location,
                    'phone':obj.phone,
                    'uid':urlsafe_base64_encode(force_bytes(instance.user.id)),
                    'token':create_token.make_token(instance.user),
                    'site_logo':obj.email_template_logo,
                    'site_name':obj.site_name,
                    'site_url':obj.site_url,
                    'description':obj.description,
                }
        template='emails/success.html'
        send_email(subject,email,message,template)

class ChatModel(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE)
    receiver=models.IntegerField(blank=True,null=True)
    message=models.TextField(blank=True,null=True)
    is_read=models.BooleanField(default=False,blank=True,null=True)
    created_on=models.DateTimeField(default=now)
    class Meta:
        db_table='chat_tbl'
        verbose_name_plural='chat_tbl'
    def __str__(self)->str:
        return f'{self.sender.get_full_name()} chat info'

@receiver(post_save, sender=ChatModel)
def create_updates_info(sender, instance, created, **kwargs):
    if created:
        channel_layer=get_channel_layer()
        user=User.objects.get(id__exact=instance.receiver)
        async_to_sync(channel_layer.group_send)(
                #room name
                "notification_%s" %user.username,
                {
                    'type': 'send_notification',
                    'activity':json.dumps({'username':instance.sender.username,'profile':instance.sender.extendedauthuser.profile_pic.url,'message':True,'title':'New message','icon':'<i class="ti-comments"></i>','activity':instance.message,'time':'just now'})
                }
        )