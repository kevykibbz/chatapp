from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import *
from .forms import *
from django import forms
import datetime
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth.forms import User
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.auth.hashers import check_password
from django.core.validators import FileExtensionValidator,URLValidator
from installation.forms import SiteModel
from django.contrib.auth import authenticate
import re
from urllib.parse import urlparse
from ckeditor.fields import RichTextFormField
from ckeditor_uploader.fields import RichTextUploadingFormField


options=[
            ('---Select gender---',
                    (
                        ('Male','Male'),
                        ('Female','Female'),
                        ('Other','Other'),
                    )
            ),
        ]
class UserResetPassword(PasswordResetForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter email address'}),error_messages={'required':'Email address is required'})

    def clean_email(self):
        email=self.cleaned_data['email']
        if  not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email address does not exist')
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError('Invalid email address')
        return email



#ChooseForm
class ChooseForm(UserChangeForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'style':'height:50px;', 'aria-required':'true','class':'form-control','placeholder':'Username ','aria-label':'username'}),error_messages={'required':'Username  is required'})

    class Meta:
        model=User
        fields=['username']

    def clean_username(self):
        username=self.cleaned_data['username']
        if self.instance.username:
            if username != self.instance.username:
                if User.objects.filter(username=username).exists():
                    raise forms.ValidationError('A user with this username already exists')
                return username
            else:
               return username
        else:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('A user with this username already exists')
            return username



class UserLoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'style':'height:50px;', 'aria-required':'true','class':'form-control','placeholder':'Username ','aria-label':'username'}),error_messages={'required':'Username  is required'})
    password=forms.CharField(widget=forms.PasswordInput(attrs={'style':'height:50px;','aria-required':'true','class':'form-control login-password','placeholder':'Password','aria-label':'password','autocomplete':'on'}),error_messages={'required':'Password is required'})

    class Meta:
        model=User
        fields=['username','password',]

    def clean_username(self):
        username=self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            return username
        else:
            raise forms.ValidationError('invalid username')

class UserReg(UserCreationForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'style':'height:50px;','aria-label':'email','class':'form-control','placeholder':'Enter email address'}),error_messages={'required':'Email address is required'})
    password1=forms.CharField(min_length=6,widget=forms.PasswordInput(attrs={'style':'height:50px;','aria-label':'password1','class':'form-control','placeholder':'Enter password','autocomplete':'on'}),error_messages={'required':'Password is required','min_length':'enter atleast 6 characters long'})
    is_active=forms.BooleanField(widget=forms.CheckboxInput(attrs={'aria-label':'is_active','id':'checkbox1'}),required=False)
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'style':'height:50px;','aria-label':'password2','class':'form-control','placeholder':'Enter confirm password','autocomplete':'on'}),error_messages={'required':'Confirm password is required'})
    class Meta:
        model=User
        fields=['email','password1','password2','is_active',]


    def clean_email(self):
        email=self.cleaned_data['email']
        if self.instance.email:
            if email != self.instance.email:
                if User.objects.filter(email=email).exists():
                    raise forms.ValidationError('A user with this email already exists.')
                try:
                    validate_email(email)
                except ValidationError as e:
                    raise forms.ValidationError('Invalid email address.')
                return email
            else:
               return email
        else:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('A user with that email already exist')
            try:
                validate_email(email)
            except ValidationError as e:
                raise forms.ValidationError('Invalid email address')
            return email

    def clean_username(self):
        username=self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('A user with this username already exists')
        return username

class ExtEmailReg(forms.ModelForm):
    category=forms.CharField(widget=forms.EmailInput(attrs={'hidden':True,'class':'form-control input-rounded','placeholder':'Email address','aria-label':'category'}),error_messages={'required':'Category is required'})
    class Meta:
        model=ExtendedAuthUser
        fields=['category',]

#profileForm
class CurrentStaffLoggedInUserProfileChangeForm(UserChangeForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-rounded'}),required=False)
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-rounded','aria-label':'last_name'}),required=False)
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-rounded','placeholder':'Username ','aria-label':'username'}),required=False)
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control input-rounded','aria-label':'email'}),required=False)
    is_active=forms.BooleanField(widget=forms.CheckboxInput(attrs={'aria-label':'is_active','id':'checkbox1'}),required=False)
    class Meta:
        model=User
        fields=['first_name','last_name','email','is_active','username',]


    def clean_first_name(self):
        first_name=self.cleaned_data['first_name']
        if first_name and not str(first_name).isalpha():
            raise forms.ValidationError('only characters are allowed.')
        return first_name
    
    def clean_last_name(self):
        last_name=self.cleaned_data['last_name']
        if last_name and not str(last_name).isalpha():
                raise forms.ValidationError('only characters are allowed.')
        return last_name

    def clean_email(self):
        email=self.cleaned_data['email']
        if email and email != self.instance.email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('A user with this email already exists.')
            try:
                validate_email(email)
            except ValidationError as e:
                raise forms.ValidationError('Invalid email address.')
            return email
        else:
           return email

    def clean_username(self):
        username=self.cleaned_data['username']
        if username and username != self.instance.username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('A user with this username already exists')
            return username
        return username

class UserPasswordChangeForm(UserCreationForm):
    oldpassword=forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'on','aria-required':'true','class':'form-control input-rounded','placeholder':'Old password','aria-label':'oldpassword'}),error_messages={'required':'Old password is required','min_length':'enter atleast 6 characters long'})
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'on','aria-required':'true','class':'form-control input-rounded','placeholder':'New password Eg Example12','aria-label':'password1'}),error_messages={'required':'New password is required','min_length':'enter atleast 6 characters long'})
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'on','aria-required':'true','class':'form-control input-rounded','placeholder':'Confirm new password','aria-label':'password2'}),error_messages={'required':'Confirm new password is required'})

    class Meta:
        model=User
        fields=['password1','password2']
    
    def clean_oldpassword(self):
        oldpassword=self.cleaned_data['oldpassword']
        if not self.instance.check_password(oldpassword):
            raise forms.ValidationError('Wrong old password.')
        else:
           return oldpassword


class ProfilePicForm(forms.ModelForm):
    profile_pic=forms.ImageField(
                                widget=forms.FileInput(attrs={'class':'profile','accept':'image/*', 'onchange':'this.form.submit();','id':'profileImage'}),
                                required=False,
                                validators=[FileExtensionValidator(['jpg','jpeg','png','gif'],message="Invalid image extension",code="invalid_extension")]
                                )
    cover_pic=forms.ImageField(
                                widget=forms.FileInput(attrs={'class':'profile','accept':'image/*', 'onchange':'this.form.submit();','id':'file-up'}),
                                required=False,
                                validators=[FileExtensionValidator(['jpg','jpeg','png','gif'],message="Invalid image extension",code="invalid_extension")]
                                )
    class Meta:
        model=ExtendedAuthUser
        fields=['profile_pic','cover_pic',]

# admin profileForm
class CurrentAdminExtUserProfileChangeForm(forms.ModelForm):
    phone=PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'class':'form-control input-rounded','type':'tel','aria-label':'phone','placeholder':'Phone example +25479626...'}),required=False)
    bio=forms.CharField(widget=forms.Textarea(attrs={'rows':5,'col':10,'class':'form-control','aria-label':'email'}),required=False)
    nickname=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-rounded','aria-label':'nickname'}),required=False)
    company=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-rounded','aria-label':'company'}),required=False)
    timezone=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-rounded','aria-label':'timezone'}),required=False)
    zipcode=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-rounded','aria-label':'zipcode'}),required=False)
    city=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-rounded','aria-label':'city'}),required=False)
    country=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-rounded','aria-label':'country'}),required=False)
    gender=forms.ChoiceField(choices=options,required=False,widget=forms.Select(attrs={'class':'form-control show-tick ms select2','placeholder':'Gender'}))
    birthday=forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','aria-label':'birthday','type':'date'}),required=False)   
    profile_pic=forms.ImageField(
                                widget=forms.FileInput(attrs={'class':'profile','accept':'image/*','hidden':True}),
                                required=False,
                                validators=[FileExtensionValidator(['jpg','jpeg','png','gif'],message="Invalid image extension",code="invalid_extension")]
                                )
    class Meta:
        model=ExtendedAuthUser
        fields=['zipcode','timezone','phone','profile_pic','bio','nickname','birthday','gender','company','country','city',]

    
    def clean_phone(self):
        phone=self.cleaned_data['phone']
        if phone != self.instance.phone:
            if ExtendedAuthUser.objects.filter(phone=phone).exists():
                raise forms.ValidationError('A user with this phone number already exists.')
            else:
                return phone
        else:
           return phone 

class ActionForm(forms.ModelForm):
    are_you_married=forms.BooleanField(widget=forms.CheckboxInput(attrs={'aria-label':'are_you_married','id':'checkbox10'}),required=False)
    are_you_available_for_chat=forms.BooleanField(widget=forms.CheckboxInput(attrs={'aria-label':'are_you_available_for_chat','id':'checkbox11'}),required=False)
    are_you_working=forms.BooleanField(widget=forms.CheckboxInput(attrs={'aria-label':'are_you_working','id':'checkbox12'}),required=False)
    are_you_athletic=forms.BooleanField(widget=forms.CheckboxInput(attrs={'aria-label':'are_you_athletic','id':'checkbox13'}),required=False)
    are_you_studying=forms.BooleanField(widget=forms.CheckboxInput(attrs={'aria-label':'are_you_studying','id':'checkbox14'}),required=False)
    class Meta:
        model=ExtendedAuthUser
        fields=['are_you_married','are_you_available_for_chat','are_you_working','are_you_athletic','are_you_studying',]

class SiteForm(forms.ModelForm):
    site_name=forms.CharField(widget=forms.EmailInput(attrs={'aria-label':'site_name','class':'form-control input-rounded','placeholder':'Site name'}),error_messages={'required':'Site Name is required'})
    description=forms.CharField(widget=forms.Textarea(attrs={'aria-label':'description','class':'form-control','placeholder':'Site Description'}),error_messages={'required':'Site Description is required'})
    theme_color=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'theme_color','class':'form-control gradient-colorpicker input-rounded','placeholder':'Site Theme Color eg #ff0000'}),required=False)
    key_words=forms.CharField(widget=forms.TextInput(attrs={'data-role':'tagsinput','aria-label':'key_words','class':'form-control input-rounded ','placeholder':'Site Keywords'}),required=False)
    site_url=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'site_url','class':'form-control input-rounded','placeholder':'Site URL'}),error_messages={'required':'Site URL is required'})
    favicon=forms.ImageField(
                                widget=forms.FileInput(attrs={'aria-label':'favicon','class':'custom-file-input','id':'customFileInput','accept':'image/*','hidden':True}),
                                required=False,
                                validators=[FileExtensionValidator(['jpg','jpeg','png','ico'],message="Invalid image extension",code="invalid_extension")]
                                )
    website_logo=forms.ImageField(
                                widget=forms.FileInput(attrs={'aria-label':'website_logo','class':'custom-file-input','id':'customFileInput1','accept':'image/*','hidden':True}),
                                required=False,
                                validators=[FileExtensionValidator(['jpg','jpeg','png','ico'],message="Invalid image extension",code="invalid_extension")]
                                ) 
    login_logo=forms.ImageField(
                                widget=forms.FileInput(attrs={'aria-label':'login_logo','class':'custom-file-input','id':'customFileInput2','accept':'image/*','hidden':True}),
                                required=False,
                                validators=[FileExtensionValidator(['jpg','jpeg','png','ico'],message="Invalid image extension",code="invalid_extension")]
                                )
    footer_logo=forms.ImageField(
                                widget=forms.FileInput(attrs={'aria-label':'footer_logo','class':'custom-file-input','id':'customFileInput3','accept':'image/*','hidden':True}),
                                required=False,
                                validators=[FileExtensionValidator(['jpg','jpeg','png','ico'],message="Invalid image extension",code="invalid_extension")]
                                )
    email_template_logo=forms.ImageField(
                                widget=forms.FileInput(attrs={'aria-label':'email_template_logo','class':'custom-file-input','id':'customFileInput4','accept':'image/*','hidden':True}),
                                required=False,
                                validators=[FileExtensionValidator(['jpg','jpeg','png','ico'],message="Invalid image extension",code="invalid_extension")]
                                )
    class Meta:
        model=SiteModel
        fields=['site_name','theme_color','site_url','description','key_words','favicon','website_logo','login_logo','footer_logo','email_template_logo',]
    
    def clean_theme_color(self):
        theme_color=self.cleaned_data['theme_color']
        match=re.search(r'^#(?:[0-9a-fA-F]{1,2}){3}$',theme_color)
        if not match:
            raise forms.ValidationError('Invalid color code given')
        else:
            return theme_color
            
    def clean_site_url(self):
        site_url=self.cleaned_data['site_url']
        if URLValidator(site_url):
            return site_url
        else:
            raise forms.ValidationError('Invalid url')


#AddressConfigForm
class AddressConfigForm(forms.ModelForm):
    site_email=forms.EmailField(widget=forms.EmailInput(attrs={'aria-label':'site_email','class':'form-control input-rounded','placeholder':'Site Email Address'}),error_messages={'required':'Address is required'})
    site_email2=forms.EmailField(widget=forms.EmailInput(attrs={'aria-label':'site_email2','class':'form-control input-rounded','placeholder':'Site Additional Email Address'}),required=False)
    address=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'address','class':'form-control input-rounded'}),error_messages={'required':'Address is required'})
    location=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'location','class':'form-control input-rounded'}),error_messages={'required':'Location is required'})
    phone=PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'aria-label':'phone','class':'form-control input-rounded'},initial='KE'),required=False)
    class Meta:
        model=SiteModel
        fields=['address','location','phone','site_email','site_email2']
    
    def clean_site_email(self):
        email=self.cleaned_data['site_email']
        if self.instance.site_email:
            if email != self.instance.site_email:
                if User.objects.filter(email=email).exists():
                    raise forms.ValidationError('A user with this email already exists.')
                try:
                    validate_email(email)
                except ValidationError as e:
                    raise forms.ValidationError('Invalid email address.')
                return email
            else:
               return email
        else:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('A user with that email already exist')
            try:
                validate_email(email)
            except ValidationError as e:
                raise forms.ValidationError('Invalid email address')
            return email
    

    def clean_site_email2(self):
        email=self.cleaned_data['site_email2']
        if self.instance.site_email2:
            if email != self.instance.site_email2:
                if User.objects.filter(email=email).exists():
                    raise forms.ValidationError('A user with this email already exists.')
                try:
                    validate_email(email)
                except ValidationError as e:
                    raise forms.ValidationError('Invalid email address.')
                return email
            else:
               return email
        else:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('A user with that email already exist')
            try:
                validate_email(email)
            except ValidationError as e:
                raise forms.ValidationError('Invalid email address')
            return email


#social form
class SiteSocialForm(forms.ModelForm):
    facebook=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'facebook','class':'form-control input-rounded','placeholder':'Facebook Link'}),required=False)    
    twitter=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'twitter','class':'form-control input-rounded','placeholder':'Twitter Link'}),required=False)    
    instagram=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'instagram','class':'form-control input-rounded','placeholder':'Instagram Link'}),required=False)    
    linkedin=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'linkedin','class':'form-control input-rounded','placeholder':'Linkedin Link'}),required=False)   
    youtube=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'youtube','class':'form-control input-rounded','placeholder':'Youtube Link'}),required=False)    
    whatsapp=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'whatsapp','class':'form-control input-rounded','placeholder':'Whats App'}),required=False)
    class Meta:
        model=SiteModel
        fields=['facebook','twitter','linkedin','instagram','youtube','whatsapp',]

    def clean_facebook(self):
        facebook=self.cleaned_data['facebook']
        if URLValidator(facebook):
                output=urlparse(facebook)
                username=output.path.strip('/')
                if not username:
                    raise forms.ValidationError('Username parameter missing')
                else:
                    return [facebook,username]
        else:
            raise forms.ValidationError('Invalid url')
    
    def clean_twitter(self):
        twitter=self.cleaned_data['twitter']
        if URLValidator(twitter):
                output=urlparse(twitter)
                username=output.path.strip('/')
                if not username:
                    raise forms.ValidationError('Username parameter missing')
                else:
                    return [twitter,username]
        else:
            raise forms.ValidationError('Invalid url')
    

    def clean_instagram(self):
        instagram=self.cleaned_data['instagram']
        if URLValidator(instagram):
                output=urlparse(instagram)
                username=output.path.strip('/')
                if not username:
                    raise forms.ValidationError('Username parameter missing')
                else:
                    return [instagram,username]
        else:
            raise forms.ValidationError('Invalid url')
    
    def clean_linkedin(self):
        linkedin=self.cleaned_data['linkedin']
        if URLValidator(linkedin):
                output=urlparse(linkedin)
                username=output.path.strip('/')
                if not username:
                    raise forms.ValidationError('Username parameter missing')
                else:
                    return [linkedin,username]
        else:
            raise forms.ValidationError('Invalid url')
    
    def clean_youtube(self):
        youtube=self.cleaned_data['youtube']
        if URLValidator(youtube):
                output=urlparse(youtube)
                username=output.path.strip('/')
                if not username:
                    raise forms.ValidationError('Channel id parameter missing')
                else:
                    return [youtube,username]
        else:
            raise forms.ValidationError('Invalid url')
    def clean_whatsapp(self):
        whatsapp=self.cleaned_data['whatsapp']
        if URLValidator(whatsapp):
            output=urlparse(whatsapp)
            username=output.path.strip('/')
            if not username:
                raise forms.ValidationError('username parameter missing')
            else:
                return [whatsapp,username]
        else:
            raise forms.ValidationError('Invalid url')

#WorkingConfigForm
class WorkingConfigForm(forms.ModelForm):
    working_days=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'working_days','class':'form-control input-rounded'}),error_messages={'required':'Working days is required'})
    working_hours=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'working_hours','class':'form-control input-rounded'}),error_messages={'required':'Working hours is required'})

    class Meta:
        model=SiteModel
        fields=['working_days','working_hours',]

class ChatForm(forms.ModelForm):
    message=forms.CharField(widget=forms.Textarea(attrs={'aria-label':'message','class':'status form-control','placeholder':'Enter message...','rows':3,'cols':'100%' ,'style':'font-size:17px;'}),error_messages={'required':'Message is required'})
    class Meta:
        model=ChatModel
        fields=['message',]


class TweetForm(forms.ModelForm):
    message=forms.CharField(widget=forms.Textarea(attrs={'aria-label':'message','class':'status form-control','maxlength':1000,'placeholder':'Whats happening?','rows':3,'cols':'100%' ,'style':'font-size:17px;'}),error_messages={'required':'Message is required'})
    tweet_image=forms.ImageField(
                                widget=forms.FileInput(attrs={'aria-label':'tweet_image','class':'profile','accept':'image/*','id':'file'}),
                                required=False,
                                validators=[FileExtensionValidator(['jpg','jpeg','png','gif'],message="Invalid image extension",code="invalid_extension")]
                                )
    class Meta:
        model=TweetModel
        fields=['message','tweet_image',]

class CommentForm(forms.ModelForm):
    comment=forms.CharField(widget=forms.Textarea(attrs={'aria-label':'comment','class':'status form-control','maxlength':1000,'placeholder':'Whats happening?','rows':3,'cols':'100%' ,'style':'font-size:17px;'}),error_messages={'required':'Comment is required'})
    class Meta:
        model=CommentModel
        fields=['comment',]


class RetweetForm(forms.ModelForm):
    retweet_message=forms.CharField(widget=forms.Textarea(attrs={'aria-label':'retweet_message','class':'status form-control','maxlength':1000,'placeholder':'Whats happening?','rows':3,'cols':'100%' ,'style':'font-size:17px;'}),error_messages={'required':'Message is required'})
    class Meta:
        model=TweetModel
        fields=['retweet_message',]
