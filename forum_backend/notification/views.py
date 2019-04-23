from django.shortcuts import render
from rest_framework import mixins,viewsets,permissions
from notification.serializers import NotificationSerializer
from notification.models import Notification

# Create your views here.

class NotificationViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = NotificationSerializer
    permission_classes = (permissions.IsAuthenticated,)



    def get_queryset(self):
        # 置获取当前用户认证的通知
        print(self.request)
        queryset = Notification.objects.filter(receiver=self.request.user).all()
        return queryset

    def perform_destroy(self, instance):
        # 覆写DELETE 方法进行软删除
        pk = self.kwargs['pk']
        instance = Notification.objects.get(id=pk)
        instance.delete()
        instance.save()

    def update(self, request, *args, **kwargs):
        # UPDATE 方法进行更改为已读
        pk = self.kwargs['pk']
        instance = Notification.objects.get(id=pk)
        if instance.receiver != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        instance.status = Notification.STATUS.read
        instance.save()
        return Response(status=status.HTTP_200_OK)
