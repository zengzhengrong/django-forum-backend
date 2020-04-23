from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)
from rest_framework import generics,permissions,views,status
from rest_framework.response import Response
from .serializers import (LoginSerializer,JWTSerializer,RegisterSerializer,PasswordResetSerializer,
						PasswordResetConfirmSerializer,PasswordChangeSerializer,VerifyRegisterEmailSerializer,
						ActiveConfirmSerilizer)
from rest_framework_jwt.settings import api_settings
from utils.jwt import jwt_encode
from user.tasks import preform_send_active_email
# from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings as jwt_settings
from datetime import datetime, timedelta
from utils.signer import signer
from threading import Thread
from utils.token_required import token_required,method_decorator

# jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
# jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
# jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

class Login(generics.GenericAPIView):
	'''
	二选一登陆方式:username或者email  
	生成token的有效期为600s(5分钟)
	当token失效时，服务端后端session（这个Django默认是7天）也随之删除
	'''
	permission_classes = (permissions.AllowAny,)
	serializer_class = LoginSerializer

	def process_login(self):
		django_login(self.request, self.user)

	def login(self):
		self.user = self.serializer.validated_data.get('user')
		self.is_active = self.serializer.validated_data.get('active')
		if self.is_active:
			self.token = jwt_encode(self.user)
			self.process_login()

	def get_response(self):
		if self.is_active is False:
			serializer_class = ActiveConfirmSerilizer
			data = {
					'message':'登陆失败:您的账号未激活！激活邮件已发送至您的注册邮箱'
					}
			serializer = serializer_class(instance=data)
			signature = Register.generate_signature(self.user.username)

			# celery asyn task
			preform_send_active_email(self.user,signature)

			return Response(serializer.data,status=status.HTTP_403_FORBIDDEN)

		elif (self.is_active and self.user):
			serializer_class = JWTSerializer
			data = {
					'message':'登陆成功',
					'user': self.user,
					'type': 'Bearer',
					'token': self.token,
					'token_with_type': f'Bearer {self.token}'
					}
			serializer = serializer_class(instance=data,context={'request': self.request})
			response = Response(serializer.data, status=status.HTTP_200_OK)

			if jwt_settings.JWT_AUTH_COOKIE:
				expiration = (datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA)
				response.set_cookie(jwt_settings.JWT_AUTH_COOKIE,self.token,expires=expiration,httponly=True)
			return response
		
		data = {'message':'未知错误'}
		return Response(data,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	def post(self, request, *args, **kwargs):
		self.request = request
		self.serializer = self.get_serializer(data=self.request.data,context={'request': request})
		self.serializer.is_valid(raise_exception=True)
		self.login()
	
		return self.get_response()

class Logout(views.APIView):
	'''
	登出
	'''
	permission_classes = (permissions.AllowAny,)

	def post(self, request, *args, **kwargs):
		return self.logout(request)

	def logout(self, request):
		django_logout(request)

		response = Response({"detail": "成功登出"},status=status.HTTP_200_OK)
		if jwt_settings.JWT_AUTH_COOKIE:
			response.delete_cookie(jwt_settings.JWT_AUTH_COOKIE)
		return response

class Register(generics.CreateAPIView):
	'''
	注册
	'''
	serializer_class = RegisterSerializer
	permission_classes = (permissions.AllowAny,)


	def get_response_data(self, user):
		data = {
			'message':'激活邮件已发至你的注册邮箱',
			'user': user,
			'token': self.token
		}
		return JWTSerializer(instance=data,context={'request': self.request}).data

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		# print(headers)

		return Response(self.get_response_data(user),status=status.HTTP_201_CREATED,headers=headers)

	def perform_create(self, serializer):
		user = serializer.save(self.request)
		signature = self.generate_signature(user.username)

		# celery asyn task
		preform_send_active_email(user,signature)

		self.token = jwt_encode(user)
		return user

	@staticmethod
	def generate_signature(username):
		signature = signer.sign(username)
		# print(signature)
		return signature


class VerifyRegisterEmail(generics.GenericAPIView):
	'''
	注册激活确认
	'''
	serializer_class = VerifyRegisterEmailSerializer
	permission_classes = (permissions.AllowAny,)

	def post(self, request, *args, **kwargs):
		# Create a serializer instance with request.data
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		
		serializer.save()
		return Response({'detali':'你的用户已激活成功'},status=status.HTTP_200_OK)

class PasswordReset(generics.GenericAPIView):
	'''
	通过email发送重置密码密码请求
	'''
	serializer_class = PasswordResetSerializer
	permission_classes = (permissions.AllowAny,)

	def post(self, request, *args, **kwargs):
		# Create a serializer with request.data
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		# multithreading
		t = Thread(target=serializer.save,name='reset-email')
		t.start()

		return Response({"detail": "密码重置邮件已发送，请查收"},status=status.HTTP_200_OK)


class PasswordResetConfirm(generics.GenericAPIView):
	'''
	确认重置密码  
	uid和token,在邮箱的链接中已给出，前端传入  
	'''
	serializer_class = PasswordResetConfirmSerializer
	permission_classes = (permissions.AllowAny,)

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			return Response({"detail": "密码已重置，请重新登录"},status=status.HTTP_200_OK)
		return Response({"detail": "令牌失效或者过期，更改失败"},status=status.HTTP_403_FORBIDDEN)

class PasswordChange(generics.GenericAPIView):
	'''
	更改密码
	仅用户认证后才可调用
	'''
	serializer_class = PasswordChangeSerializer
	permission_classes = (permissions.IsAuthenticated,)

	@method_decorator(token_required)
	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response({"detail": "新密码已生效"},status=status.HTTP_200_OK)