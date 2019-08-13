from django.shortcuts import render
from rest_framework import mixins,viewsets,permissions,status
from notification.serializers import NotificationSerializer
from notification.models import Notification
from rest_framework.response import Response

# Create your views here.

class NotificationViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = NotificationSerializer
    permission_classes = (permissions.IsAuthenticated,)



    def get_queryset(self):
        # 置获取当前用户认证的通知
        print(self.request.session.items())
        # print(dir(self.request.session))
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
