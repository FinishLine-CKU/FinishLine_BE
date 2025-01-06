from .base import *
import os

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'FinishLine_DB',
        'USER': 'FinishLine',
        'PASSWORD': 'finishline',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}