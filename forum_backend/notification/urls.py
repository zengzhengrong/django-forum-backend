from django.urls import path
from notification import views

app_name = 'notification'

notification_user_list = views.NotificationViewSet.as_view({'get':'list'})
notification_detail = views.NotificationViewSet.as_view({
	'get':'retrieve',
	'put':'update',
	'patch':'partial_update',
	'delete':'destroy'
	})


urlpatterns = [
    path('user/list/', notification_user_list, name='notification-list'),
    path('detail/<int:pk>', notification_detail, name='notification-detail'),
]

