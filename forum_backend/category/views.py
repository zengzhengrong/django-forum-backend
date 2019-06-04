from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from category.models import Category
from category.serializers import CategorySerializer
from category.permissions import IsAdmin
from datetime import datetime
from rest_framework.response import Response
from utils.models_field import json,TimeJsonEncoder
# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdmin,)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # 更新历史记录
        data = {
            'datetime':datetime.now(),
            'name':instance.name
        }

        if not instance.history: 
            instance.history = []
            instance.history.append(data)
        else:
            instance.history = json.dumps(instance.history,TimeJsonEncoder)

        serializer = self.get_serializer(instance, data=request.data, partial=partial) # 更新数据
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()