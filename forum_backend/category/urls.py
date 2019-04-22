from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from category import views

app_name = 'category'

category_list = views.CategoryViewSet.as_view({'get':'list','post':'create'})
category_detail = views.CategoryViewSet.as_view({
	'get':'retrieve',
	'put':'update',
	'patch':'partial_update',
	'delete':'destroy'
	})


urlpatterns = format_suffix_patterns([
    path('list/', category_list, name='category-list'),
    path('detail/<int:pk>', category_detail, name='category-detail'),
])