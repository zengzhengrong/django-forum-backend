from django.shortcuts import render
from rest_framework import generics,permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer,UserProfileSerializer
from user.permissions import IsUserOwnerOrReadOnly ,IsAdmin
from user.models import UserProfile

User = get_user_model()

class UserList(generics.ListAPIView):
	"""
	Get User List
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = (IsAdmin,)
	

class UserDetail(generics.RetrieveAPIView):
	"""
	Retrieve a Detail User
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer
	
	


class UserProfileUpdate(generics.UpdateAPIView):
	'''
	Update UserProfile
	'''
	queryset = UserProfile
	serializer_class = UserProfileSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsUserOwnerOrReadOnly)

	def update(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', False)
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)
		data = {
			'stats':'1',
			'profile':serializer.data
		}
		if getattr(instance, '_prefetched_objects_cache', None):
			# If 'prefetch_related' has been applied to a queryset, we need to
			# forcibly invalidate the prefetch cache on the instance.
			instance._prefetched_objects_cache = {}

		return Response(data)