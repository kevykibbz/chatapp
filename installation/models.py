from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.utils.timezone import now
import environ
env=environ.Env()
environ.Env.read_env()

# Create your models here.

class SiteModel(models.Model):
    user=models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)
    site_name=models.CharField(null=True,blank=True,max_length=100,default=env('SITE_NAME'))
    site_email=models.CharField(null=True,blank=True,max_length=100,default=env('SITE_EMAIL'))
    site_email2=models.CharField(null=True,blank=True,max_length=100,default=env('SITE_EMAIL2'))
    theme_color=models.CharField(null=True,blank=True,max_length=100,default=env('THEME_COLOR'))
    site_url=models.URLField(null=True,blank=True,default=env('SITE_URL'))
    description=models.TextField(null=True,blank=True,default=env('SITE_DESCRIPTION'))
    key_words=models.TextField(null=True,blank=True,default=env('SITE_KEYWORDS'))
    address=models.CharField(null=True,blank=True,max_length=250,default=env('SITE_ADDRESS'))
    location=models.CharField(null=True,blank=True,max_length=250,default=env('SITE_LOCATION'))
    phone=PhoneNumberField(null=True,blank=True,verbose_name='phone',unique=False,default=env('SITE_PHONE1'))
    working_days=models.CharField(null=True,blank=True,max_length=250,default="mon-fri")
    site_content=models.CharField(null=True,blank=True,max_length=250)
    timezone=models.CharField(max_length=200,null=True,blank=True,default='Africa/Nairobi')
    working_hours=models.CharField(null=True,blank=True,max_length=250,default="8am-10pm")
    closed_days=models.CharField(null=True,blank=True,max_length=250,default="sun")
    tidio_script=models.CharField(null=True,blank=True,max_length=300,default="//code.tidio.co/yijtlq2xmcygrfhxlr5u7s30so7kl1w9.js")
    special_days=models.CharField(null=True,blank=True,max_length=250,default="sat & holidays")
    special_hours=models.CharField(null=True,blank=True,max_length=250,default="sat & holidays")
    facebook=models.CharField(null=True,blank=True,max_length=250,default=env('FACEBOOK_LINK'))
    twitter=models.CharField(null=True,blank=True,max_length=250,default=env('TWITTER_LINK'))
    instagram=models.CharField(null=True,blank=True,max_length=250,default=env('INSTAGRAM_LINK'))
    whatsapp=models.CharField(null=True,blank=True,max_length=250,default=env('WHATSAPP_LINK'))
    linkedin=models.CharField(null=True,blank=True,max_length=250,default=env('LINKEDIN_LINK'))
    youtube=models.CharField(null=True,blank=True,max_length=250,default=env('YOUTUBE_LINK'))
    favicon=models.ImageField(null=True,blank=True,upload_to='logos/',default="logos/favicon.ico")
    website_logo=models.ImageField(null=True,blank=True,upload_to='logos/',default="logos/favicon.ico")
    footer_logo=models.ImageField(null=True,blank=True,upload_to='logos/',default="logos/favicon.ico")
    email_template_logo=models.ImageField(null=True,blank=True,upload_to='logos/',default="logos/favicon.ico")
    login_logo=models.ImageField(null=True,blank=True,upload_to='logos/',default="logos/favicon.ico")
    main=models.BooleanField(default=False)
    is_installed=models.BooleanField(default=False)
    created_on=models.DateTimeField(default=now)
    class Meta:
        db_table='site_model'
        verbose_name_plural='site_model'
    def __str__(self):
        return f'{self.user.username} site variables'


