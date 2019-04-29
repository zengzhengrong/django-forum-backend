from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import UserList, UserDetail, Login, Logout , Register, PasswordResetView , PasswordResetConfirm, PasswordChange

app_name = 'user'

urlpatterns = format_suffix_patterns([
    path('list/', UserList.as_view(), name='user-list'),
    path('detail/<int:pk>', UserDetail.as_view(), name='user-detail'),
    path('login/',Login.as_view(),name='user-login'),
    path('logout/',Logout.as_view(),name='user-logout'),
    path('register/',Register.as_view(),name='user-register'),
    path('password-reset/',PasswordResetView.as_view(),name='user-password-reset'),
    path('password-reset/confirm/',PasswordResetConfirm.as_view(),name='user-password-confirm'),
    path("password-change/", PasswordChange.as_view(), name="user-password-change")
])