from django.shortcuts import render
from datetime import datetime,timedelta
from rest_framework import filters
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.exceptions import server_error
from post.serializers import PostSerializer,ListPostSerializer
from post.permissions import IsPostAuthorOrReadOnly
from post.models import Post,Category
from post.pagination import PostPagination
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
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
class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsPostAuthorOrReadOnly)
    filter_backends = (filters.SearchFilter,filters.OrderingFilter)
    pagination_class = PostPagination
    search_fields = ('title',) # 可以根据前缀符号来限制搜索，如'^title' 匹配开头，默认是模糊搜索
    ordering_fields = ('views', 'created', 'highlighted')
    parse_strtime_formaterror = None
    
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

    # def get_queryset(self):
    #     '''
    #     根据url参数来确定返回的查询集
    #     如筛选某分类下的帖子
    #     '''

    #     return 

    @swagger_auto_schema(query_serializer=ListPostSerializer)
    def list(self, request, *args, **kwargs):
        '''
        获取帖子列表
        可选参数
            search:搜索词,可以根据前缀符号来限制搜索，如'^title' 匹配开头，默认是模糊搜索
            ordering:排序 ，支持的栏位(views, created, highlighted) or (-views, -created, -highlighted) -符表示倒序
            page:页数
            page_size:一页的个数
            category_id:分类的id，只获取该分类下的帖子
            lt_datetime:只获取小于该时间的帖子，格式：%Y-%m-%dT%H:%M:%S
        '''
        params = self.request.query_params

        category_id = params.get('category_id')
        lt_datetime = params.get('lt_datetime')
        if category_id:
            self.queryset = self.queryset.filter(category__id=category_id)
        if lt_datetime:
            try:
                parse_strtime = datetime.strptime(lt_datetime,'%Y-%m-%dT%H:%M:%S')
                parse_strtime_time = parse_strtime.time()
                parse_strtime_date = parse_strtime.date()
                datetime_combine = datetime.combine(parse_strtime_date,parse_strtime_time)
                format_to_timezone = timezone.make_aware(datetime_combine,)
                self.queryset = self.queryset.filter(created__lte=format_to_timezone)
            except ValueError:
                self.parse_strtime_formaterror = True

        self.queryset = self.queryset.all()

        queryset = self.filter_queryset(self.queryset)
        # parse_strtime_formaterror response , must be behind self.get_queryset() method
        if self.parse_strtime_formaterror:
            return Response({'message':'The lt_datetime of params format error , Please check out your request'},status=403)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # def get_permissions(self):
    #     if self.action in ('create',):
    #         self.permission_classes = [permissions.IsAdminUser]
    #     return [permission() for permission in self.permission_classes]


