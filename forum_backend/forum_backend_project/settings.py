
from .base import *
import datetime
from django.urls import reverse_lazy
# Application definition

INSTALLED_APPS = INIT_APPS + [
    'rest_framework',
    'corsheaders',
    'drf_yasg',
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
# 在Common中间件前添加cors的中间件
MIDDLEWARE.insert(2,'corsheaders.middleware.CorsMiddleware')


REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 2,
    'URL_FORMAT_OVERRIDE':'format',
    'FORMAT_SUFFIX_KWARG':'format', # https://www.django-rest-framework.org/api-guide/settings/#format_suffix_kwarg
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication', 替换掉，取消csrf认证
        'utils.authentication.CsrfExemptSessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

# DATABASES Settings
DATABASES = {
    'default':env.db()
}

# 配置Swagger UI / Open API
SWAGGER_SETTINGS = {
    'LOGIN_URL': reverse_lazy('user:user-login'),
    'LOGOUT_URL': reverse_lazy('user:user-logout'),
    'DEFAULT_INFO': 'forum_backend_project.urls.swagger_info',
    'USE_SESSION_AUTH': False,
    'PERSIST_AUTH': False,
    'REFETCH_SCHEMA_WITH_AUTH': False,
    'REFETCH_SCHEMA_ON_LOGOUT': False,
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        },
        'Bearer': {
            'in': 'header',
            'name': 'Authorization',
            'type': 'apiKey',
        },
        'Query': {
            'in': 'query',
            'name': 'auth',
            'type': 'apiKey',
        },
    },
}

REDOC_SETTINGS = {
   'LAZY_RENDERING': False,
}
# 配置Swagger UI / Open API End


# 配置Logging settings
LOGGING_FORMATTERS = {
    'verbose': {'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'},
    'simple': {'format': '%(levelname)s %(message)s'}
    }
LOGGING_HANDLERS = {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            'logstash': {
                'level': 'WARNING',
                'class': 'logstash.TCPLogstashHandler',
                'host': env('ELK_LOGSTASH_HOST'),
                'port': env.int('ELK_LOGSTASH_PORT'),
                'version': 1,
                'message_type': 'django_logstash',  # 'type' field in logstash message. Default value: 'logstash'.
                'fqdn': False,  # Fully qualified domain name. Default value: false.
                'tags': ['django.request'],
            },
        }

LOGGING_LOGGERS = {
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': True,
            },
            'django.request': {
                'handlers': ['logstash'],
                'level': 'WARNING',
                'propagate': True,
            },
        }
if env.bool('ELK'):
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': LOGGING_FORMATTERS,
        'handlers': LOGGING_HANDLERS,
        'loggers': LOGGING_LOGGERS,
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
# EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = env('EMAIL_HOST_USER')

# 更改密码时需要验证旧密码
OLD_PASSWORD_FIELD_ENABLED = True

# 解决跨域问题（在添加中间件，在response头添加 Access-Control-Allow-Origin: *）
# dev 使用全允许 product 使用白名单
CORS_ORIGIN_ALLOW_ALL = True # dev
# CORS_ORIGIN_WHITELIST = ('127.0.0.1:8002',) # product 前端跑去来的服务

# 配置jwt认证
JWT_AUTH = {
    'JWT_AUTH_COOKIE': 'token',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=6000)
}
# 配置Session 过期时间 和 JWT过期时间一样
SESSION_COOKIE_AGE = 600 * 10

# 配置Celery
CELERY_BROKER_URL = env('CELERY_REDIS_URL')
#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_TASK_ROUTES = {
    'user.tasks.add': {'queue': 'math'}
    }
CELERY_RESULT_BACKEND = env('CELERY_REDIS_URL')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'