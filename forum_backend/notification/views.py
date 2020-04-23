from django.shortcuts import render
from rest_framework import mixins,viewsets,permissions,status
from notification.serializers import NotificationSerializer
from notification.models import Notification
from rest_framework.response import Response
from utils.token_required import token_required,method_decorator
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

class NotificationViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = NotificationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # @swagger_auto_schema(operation_description="partial_update description override", responses={404: 'slug not found'})
    @method_decorator(token_required)
    def list(self, request, *args, **kwargs):
        '''
        获取当前用户认证的通知(需要登陆)
        '''
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        # 置获取当前用户认证的通知
        # print(self.request.session.items())
        # print(getattr(self, 'swagger_fake_view', False))
        if getattr(self, 'swagger_fake_view', False):
            # queryset just for schema generation metadata
            return Notification.objects.none()
        queryset = Notification.objects.filter(receiver=self.request.user).all()
        return queryset


    def update(self, request, *args, **kwargs):
        # UPDATE 方法进行更改为已读，且只允许修改为已读
        pk = self.kwargs['pk']
        instance = Notification.objects.get(id=pk)
        if instance.receiver != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        instance.status = Notification.STATUS.read
        instance.save()
        return Response(status=status.HTTP_200_OK)
