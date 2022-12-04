from pathlib import Path
import environ
import os
env=environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY =env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = ['localhost','127.0.0.1','my-chat-pal.herokuapp.com','www.my-chat-pal.herokuapp.com',]


# Application definition

SESSION_EXPIRE_AT_BROWSER_CLOSE=True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS=7
ACCOUNT_EMAIL_REQUIRED=True
ACCOUNT_LOGIN_ATTEMPT_LIMIT=4
SITE_ID=3
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]
INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'clearcache',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'installation.apps.InstallationConfig',
    'django.contrib.humanize',
    'channels',
    'phonenumber_field',
    'mathfilters',
    'online_users',
    'rest_framework',
    'errors.apps.ErrorsConfig',
    'panel.apps.PanelConfig',
    'django.contrib.sites', #social app 
    'allauth', #social app
    'allauth.account', #social app
    'allauth.socialaccount', #social app
    'allauth.socialaccount.providers.google', #social app
    'allauth.socialaccount.providers.twitter', #social app
    'allauth.socialaccount.providers.instagram', #social app
    'django_cleanup.apps.CleanupConfig',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'chatapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #str(os.path.split(os.getcwd())[1])+'.site_constants.export_vars',
                'chatapp.site_constants.export_vars',
            ],
        },
    },
]

WSGI_APPLICATION = 'chatapp.wsgi.application'
ASGI_APPLICATION = 'chatapp.asgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DATABASES = {
    'default': 
            {

                'ENGINE': 'django.db.backends.postgresql',
                'NAME':env('DATABASE_NAME'),
                'USER':env('DATABASE_USER'),
                'PASSWORD':env('DATABASE_PASSWORD'),
                'HOST':env('DATABASE_HOST'),
                'PORT':env('DATABASE_PORT'),
            }
}

# DATABASES = {
#    'default': 
#             {

#                 'ENGINE': 'mysql.connector.django',
#                 'NAME':'chatapp',
#                 'USER':'root',
#                 'PASSWORD':'',
#                 'HOST':'localhost',
#                 'PORT':3306,
#                 'OPTIONS':
#                 {
#                     'autocommit':True,
#                 },
#             }
# }

import dj_database_url
db_from_env=dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS':
        {
            'min_length':6,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME':'panel.validators.NumberValidator',
        'OPTIONS':
        {
            'min_length':2,
        },
    },
    {
        'NAME':'panel.validators.UpperCaseValidator',
    },
    {
        'NAME':'panel.validators.LowerCaseValidator',
    },
]



#login
LOGIN_URL='/accounts/login/'
LOGIN_REDIRECT_URL='/dashboard'
LOGOUT_REDIRECT_URL='/accounts/login/'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL='/media/'


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if DEBUG:
    STATICFILES_DIRS=[os.path.join(BASE_DIR,'static')]
else:
    STATIC_ROOT=os.path.join(BASE_DIR,'static')


MEDIA_ROOT=os.path.join(BASE_DIR,'media')


BASE_URL=env('BASE_URL')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EEMAIL_HOST=env('EMAIL_HOST')
EMAIL_HOST_USER=env('EMAIL_USER')
EMAIL_HOST_PASSWORD=env('EMAIL_PASSWORD')
EMAIL_USE_TLS=True
EMAIL_PORT=587 
DEFAULT_FROM_EMAIL=EMAIL_HOST_USER

SESSION_ENGINE='django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS='default'
CACHE_TTL = 60 * 15

#cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('REDIS_URL','redis://127.0.0.1:6379/1'),
        #"LOCATION":"redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

#channels
CHANNEL_LAYERS={
    'default':{
        'BACKEND':'channels_redis.core.RedisChannelLayer',
        #'BACKEND':'channels.layers.InMemoryChannelLayer',
        'CONFIG':{
            'hosts':[os.environ.get('REDIS_URL','redis://localhost:6379')],
            #'hosts':['redis://localhost:6379',],
        },
    },
}
