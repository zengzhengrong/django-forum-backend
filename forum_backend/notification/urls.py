from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from notification import views

app_name = 'notification'

notification_user_list = views.NotificationViewSet.as_view({'get':'list'})
notification_detail = views.NotificationViewSet.as_view({
	'get':'retrieve',
	'put':'update',
	'patch':'partial_update',
	'delete':'destroy'
	})


urlpatterns = format_suffix_patterns([
    path('user/list/', notification_user_list, name='notification-list'),
    path('detail/<int:pk>', notification_detail, name='notification-detail'),
])

