"""
Django settings for Scence project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2i@v)tjqty!-!9r*c!8rni_z#4oy5137%9u=#lp!gv(0*me_*0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ScenceView.apps.ScenceViewConfig',
    'TrafficView.apps.TrafficviewConfig',
    'weather.apps.WeatherConfig',
    'internet.apps.InternetConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Scence.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(BASE_DIR, 'templates/Weather')
            , os.path.join(BASE_DIR, 'templates/Traffic'), os.path.join(BASE_DIR, 'templates/JingQu'), ]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Scence.wsgi.application'

DATABASES = {
    'default': {

    },

    'webdata': {
        'ENGINE': 'django.db.backends.mysql',
        "NAME": "webdata",  # 数据库名
        'USER': "root",  # 用户
        'PASSWORD': 'lzs87724158',
        'HOST': '',  # 数据库主机，留空默认为localhost
        'PORT': '3306',  # 数据库端口
    },
    'trafficdatabase': {
        'ENGINE': 'django.db.backends.mysql',
        "NAME": "trafficdatabase",  # 数据库名
        'USER': "root",  # 用户
        'PASSWORD': 'lzs87724158',
        'HOST': '',  # 数据库主机，留空默认为localhost
        'PORT': '3306',  # 数据库端口
    },
    'weather': {
        'ENGINE': 'django.db.backends.mysql',
        "NAME": "weather",  # 数据库名
        'USER': "root",  # 用户
        'PASSWORD': 'lzs87724158',
        'HOST': '',  # 数据库主机，留空默认为localhost
        'PORT': '3306',  # 数据库端口
    },

}

DATABASE_ROUTERS = ['Scence.authrouter.AuthRouter']
DATABASE_APPS_MAPPING = {
    "ScenceView": "webdata",
    "TrafficView": "trafficdatabase",
    "weather": "weather",
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
