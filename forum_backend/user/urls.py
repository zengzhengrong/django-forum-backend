from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import UserList, UserDetail,UserProfileUpdate

app_name = 'user'

urlpatterns = format_suffix_patterns([
    path('list/', UserList.as_view(), name='user-list'),
    path('detail/<int:pk>', UserDetail.as_view(), name='user-detail'),
    path('update/<int:pk>', UserProfileUpdate.as_view(),name='user-update')
])