import os
from pathlib import Path
from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-sj_)y5hp!iw71gb%a21k)y_m@^@thu_sn2)68yfb(@dd5hd2)r'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tasks',
    'users',
    'projects',
    'telegram_integration',
    'vk_integration',
    'reports'
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

ROOT_URLCONF = 'task_management_service.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'task_management_service.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

LOGIN_REDIRECT_URL = '/tasks/'
LOGOUT_REDIRECT_URL = '/tasks/'
LOGIN_URL = '/users/login/'

TELEGRAM_BOT_TOKEN = '8676363348:AAFaJVjBdVLgPoOBTfCHXN-q-3dGa5q2LVg'
VK_GROUP_TOKEN = 'vk1.a.Ot4IF3crcWcXPW7vOV3DpLPIWqir5910bQ6p2uV5TtgbovcYpqqD9ljUmzkdjyXxBaHOb5l7rKy3Mq5SmwXHzoIHBJ0AbUVvmuz5XzQ7DY4coGHNSg0YKaDS7-PUBj-fsGrIsPuege0CLhilSEpGGelYf69u7qYvJPQllaEivqz8QT01B--p7nZsDf-iLY6wo91i3RzuKqvLe7dEmOmZWg'
VK_GROUP_ID = 237972255 

CELERY_BEAT_SCHEDULE = {
    'notify-overdue-tasks-every-10-minutes': {
        'task': 'tasks.tasks.notify_overdue_tasks',
        'schedule': crontab(minute='*/10'),
    },
}

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'