
from .base import *
import datetime


# Application definition

INSTALLED_APPS = INIT_APPS + [
    'rest_framework',
    'user',
    'category',
    'comment',
    'post',
    'notification'
    
]

MIDDLEWARE = INIT_MIDDLEWARE + [
    'utils.middleware.TokenCookieExpireMiddleware',
    'utils.middleware.UserLogMiddleware',
]

REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 2,
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

# 配置AUTH
AUTH_USER_MODEL = 'auth.user'
AUTH_USER_ADMINS = ['zzr']

# 配置邮箱
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_SUBJECT_PREFIX = 'django-forum-email'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = env('EMAIL_HOST_USER')

# 更改密码时需要验证旧密码
OLD_PASSWORD_FIELD_ENABLED = True

# 配置jwt认证
JWT_AUTH = {
    'JWT_AUTH_COOKIE': 'token',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=600)
}

# 配置Celery
CELERY_BROKER_URL = 'redis://'
#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_TASK_ROUTES = {
    'user.tasks.add': {'queue': 'math'}
    }
CELERY_RESULT_BACKEND = 'redis://'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'