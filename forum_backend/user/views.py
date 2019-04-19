from django.shortcuts import render
from rest_framework import generics,permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
User = get_user_model()

class UserList(generics.ListAPIView):
	"""
	Get User List
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
	"""
	Retrieve a Detail User
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer