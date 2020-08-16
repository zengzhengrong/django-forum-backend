from django.contrib.auth import get_user_model
from user.permissions import IsUserOwnerOrReadOnly,IsAdmin
from user.models import UserProfile,UserLog
from rest_framework import viewsets, mixins,parsers
from .serializers import UserSerializer,UserProfileSerializer,UserLogSerializer,PutUserProfileSerializer
from .pagination import UserLogPagination
from utils.token_required import token_required,method_decorator
from drf_yasg.utils import swagger_auto_schema

User = get_user_model()

class UserModelViewSet(viewsets.ReadOnlyModelViewSet,mixins.UpdateModelMixin):
    '''
    实现LRU  list() retrieve() update()
    list -> admin
    retrieve -> any
    update -> user and admin
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,IsUserOwnerOrReadOnly)
    parser_classes=(parsers.MultiPartParser,)

    @method_decorator(token_required)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(token_required)
    @swagger_auto_schema(request_body=PutUserProfileSerializer,)
    def update(self, request, *args, **kwargs):
        self.serializer_class = UserProfileSerializer
        return super().update(request, *args, **kwargs)

    def get_object(self):
        instance = super().get_object()
        if self.request.method == 'PUT':
            return instance.profile
        return instance

class UserLogModelViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    '''
    获取用户日志列表
    list -> admin
    
    '''
    queryset = UserLog.objects.all()
    serializer_class = UserLogSerializer
    permission_classes = (IsAdmin,)
    pagination_class = UserLogPagination

    @method_decorator(token_required)
    def list(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')

        if user_id == 0:
            # 0 表示查询匿名用户
            self.queryset = UserLog.objects.filter(username='AnonymousUser').all()
            
        if user_id and user_id != 0:
            try:
                user = User.objects.get(id=user_id)
                self.queryset = UserLog.objects.filter(username=user.username).all()
            except User.DoesNotExist:
                # 返回一个空列表，当找不到该user时
                self.queryset = []

        return super().list(request, *args, **kwargs)

