from django.urls import path
from .views import (Login, Logout , Register, PasswordReset , PasswordResetConfirm, 
                    PasswordChange,VerifyRegisterEmail)
from . import viewset

app_name = 'user'

user_list = viewset.UserModelViewSet.as_view({'get':'list'})
user_detail = viewset.UserModelViewSet.as_view({
    'get':'retrieve',
    'put':'update',
    'patch':'partial_update'
})

user_logs = viewset.UserLogModelViewSet.as_view({'get':'list'})

urlpatterns = [
    path('list/', user_list, name='user-list'),
    path('detail/<int:pk>', user_detail, name='user-detail'),
    path('logs/', user_logs, name='user-logs'),
    path('logs/<int:pk>', user_logs, name='user-specify-logs'),
    path('login/',Login.as_view(),name='user-login'),
    path('logout/',Logout.as_view(),name='user-logout'),
    path('register/',Register.as_view(),name='user-register'),
    path('password-reset/',PasswordReset.as_view(),name='user-password-reset'),
    path('password-reset/confirm/',PasswordResetConfirm.as_view(),name='user-password-confirm'),
    path("password-change/", PasswordChange.as_view(), name="user-password-change"),
    path("register/active-confirm/", VerifyRegisterEmail.as_view(), name="user-register-active-confirm")
]