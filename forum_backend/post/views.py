from django.shortcuts import render
from rest_framework import filters
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from post.serializers import PostSerializer
from post.permissions import IsPostAuthorOrReadOnly
from post.models import Post,Category

# Create your views here.

# class PostFilter(filters.FilterSet):
#     category = filters.ModelChoiceFilter(queryset=Category.objects.all())
#     sort = filters.OrderingFilter(fields=('created',),field_labels={'created':'排序'})
#     # crated_date = filters.NumberFilter(field_name='created', lookup_expr='date')
#     min_created = filters.DateFilter(field_name='created', lookup_expr='date__gte')
#     max_created = filters.DateFilter(field_name='created', lookup_expr='date__lte')

#     class Meta:
#         model = Post
#         fields = []
class PostViewSets(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsPostAuthorOrReadOnly)
    filter_backends = (filters.SearchFilter,filters.OrderingFilter)
    search_fields = ('title',) # 可以根据前缀符号来限制搜索，如'^title' 匹配开头，默认是模糊搜索
    ordering_fields = ('views', 'created', 'highlighted')

    def perform_create(self, serializer):        
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """
        覆写 添加 点击阅读量+1
        """
        instance = self.get_object()
        instance.add_views()
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        '''
        根据url参数来确定返回的查询集
        如筛选某分类下的帖子
        '''
        params = self.request.query_params
        queryset = self.queryset
        # print (params) # 这里有个小问题，在发出请求后这个函数会执行两遍
        category_id = params.get('category_id')
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        return queryset

    # def get_permissions(self):
    #     if self.action in ('create',):
    #         self.permission_classes = [permissions.IsAdminUser]
    #     return [permission() for permission in self.permission_classes]


