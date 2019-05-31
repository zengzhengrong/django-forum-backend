"""forum_backend_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.views.generic import TemplateView
from rest_framework_jwt import views as jwt_views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def ApiRoot(request,format=None):
	return Response({
		'users':reverse('user:user-list',request=request,format=format),
        'user-logs':reverse('user:user-logs',request=request,format=format),
        'categorys':reverse('category:category-list',request=request,format=format),
		'posts':reverse('post:post-list',request=request,format=format),
        'notification':reverse('notification:notification-list',request=request,format=format),
        'comments':reverse('comment:comment-list',request=request,format=format),
        'authentication':{
            'login':reverse('user:user-login',request=request,format=format),
            'logout':reverse('user:user-logout',request=request,format=format),
            'register':reverse('user:user-register',request=request,format=format),
            'register-active-confirm':reverse('user:user-register-active-confirm',request=request,format=format),
            'send-reset-password-email':reverse('user:user-password-reset',request=request,format=format),
            'reset-password-confirm':reverse('user:user-password-confirm',request=request,format=format),
            'password-change':reverse('user:user-password-change',request=request,format=format)
            }
		})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('',ApiRoot,name='api-index'),
    path('category/', include('category.urls')),
    path('notification/', include('notification.urls')),
    path('post/', include('post.urls')),
    path('comment/', include('comment.urls')),
    path('user/',include('user.urls')),
    # this url is used to generate email content uidb64 and token for password_reset_confirm
    path('user/password-reset/confirm/<uidb64>/<token>/',TemplateView.as_view(template_name="password_reset_confirm.html"),name='password_reset_confirm'),
    # this url is used to generate email content key for register_confirm
    path('user/register-confirm-email/<signature>/', TemplateView.as_view(),name='register_confirm')
]
