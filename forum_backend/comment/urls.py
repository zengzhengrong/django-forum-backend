from django.urls import path
from comment import views
# from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'comment'

comment_list = views.CommentViewSet.as_view({'get':'list','post':'create'})
comment_detail = views.CommentViewSet.as_view({
	'get':'retrieve',
	'put':'update',
	'patch':'partial_update',
	'delete':'destroy'
	})

urlpatterns = [
    path('list/', comment_list, name='comment-list'),
    path('detail/<int:pk>', comment_detail, name='comment-detail')

]