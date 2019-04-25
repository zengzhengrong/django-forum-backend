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
from django.urls import path,include
from rest_framework_jwt import views as jwt_views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def ApiRoot(request,format=None):
	return Response({
		'users':reverse('user:user-list',request=request,format=format),
        'categorys':reverse('category:category-list',request=request,format=format),
		'posts':reverse('post:post-list',request=request,format=format),
        'notification':reverse('notification:notification-list',request=request,format=format),
        'comments':reverse('comment:comment-list',request=request,format=format)
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
    path('rest-auth/',include('rest_auth.urls')),
    path('rest-auth/registration',include('rest_auth.registration.urls'))
    # path('api/token/', jwt_views.obtain_jwt_token, name='token_obtain_pair'),
    # path('api/token/refresh/', jwt_views.refresh_jwt_token, name='token_refresh'),
]
