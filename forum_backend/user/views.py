from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)
from django.shortcuts import render
from rest_framework import generics,permissions,views,status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer,UserProfileSerializer,LoginSerializer,JWTSerializer
from user.permissions import IsUserOwnerOrReadOnly ,IsAdmin
from user.models import UserProfile
from rest_framework_jwt.settings import api_settings
from utils.jwt import jwt_encode
# from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings as jwt_settings
from datetime import datetime

User = get_user_model()

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

class UserList(generics.ListAPIView):
	"""
	Get User List
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = (IsAdmin,)
	


class UserDetail(generics.RetrieveUpdateAPIView):
	"""
	Retrieve a Detail User
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer

	def put(self, request, *args, **kwargs):
		self.serializer_class = UserProfileSerializer
		return self.update(request, *args, **kwargs)

	def get_object(self):
		instance = super().get_object()
		if self.request.method == 'PUT':
			return instance.profile
		return instance

class Login(generics.GenericAPIView):
	'''
	二选一登陆方式：  
	username或者email  
	生成token的有效期为300s(5分钟)
	'''
	permission_classes = (permissions.AllowAny,)
	serializer_class = LoginSerializer

	def process_login(self):
		django_login(self.request, self.user)

	def login(self):
		self.user = self.serializer.validated_data['user']
		self.token = jwt_encode(self.user)
		self.process_login()

	def get_response(self):
		serializer_class = JWTSerializer
		data = {
				'user': self.user,
				'token': self.token
				}
		serializer = serializer_class(instance=data,context={'request': self.request})
		response = Response(serializer.data, status=status.HTTP_200_OK)

		if jwt_settings.JWT_AUTH_COOKIE:
			expiration = (datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA)
			response.set_cookie(jwt_settings.JWT_AUTH_COOKIE,self.token,expires=expiration,httponly=True)
		return response

	def post(self, request, *args, **kwargs):
		self.request = request
		self.serializer = self.get_serializer(data=self.request.data,context={'request': request})
		self.serializer.is_valid(raise_exception=True)
		self.login()
	
		return self.get_response()

class Logout(views.APIView):
	permission_classes = (permissions.AllowAny,)

	def post(self, request, *args, **kwargs):
		return self.logout(request)

	def logout(self, request):
		django_logout(request)

		response = Response({"detail": "Successfully logged out."},status=status.HTTP_200_OK)
		if jwt_settings.JWT_AUTH_COOKIE:
			response.delete_cookie(jwt_settings.JWT_AUTH_COOKIE)
		return response