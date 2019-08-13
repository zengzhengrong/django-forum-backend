from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from post import views

app_name = 'post'

post_list = views.PostViewSet.as_view({'get':'list','post':'create'})
post_detail = views.PostViewSet.as_view({
	'get':'retrieve',
	'put':'update',
	'patch':'partial_update',
	'delete':'destroy'
	})


urlpatterns = format_suffix_patterns([
    path('list/', post_list, name='post-list'),
    path('detail/<int:pk>', post_detail, name='post-detail'),
])

