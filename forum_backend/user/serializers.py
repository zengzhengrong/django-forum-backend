from rest_framework import serializers,exceptions
from rest_framework.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.contrib.auth.tokens import default_token_generator
from .models import UserProfile , UserLog
from utils.signer import signer,SignatureExpired,BadSignature

User = get_user_model()

class UserLogSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    
    class Meta:
        model = UserLog
        fields = '__all__'


    def get_username(self,obj):
        if obj.username != 'AnonymousUser':
            user = User.objects.get(username=obj.username)
            data = UserSimpleSerializer(user).data
            return data
        return obj.username


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        read_only_fields = ('user','vip','last_login_ip','register_ip','start','end')
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user:user-detail')
    nickname = serializers.CharField(source='profile.nickname')
    avatar = serializers.FileField(source='profile.avatar')
    description = serializers.CharField(source='profile.description')
    last_login_ip = serializers.IPAddressField(source='profile.last_login_ip',read_only=True)
    register_ip = serializers.IPAddressField(source='profile.register_ip',read_only=True)
    start = serializers.DateTimeField(source='profile.start',read_only=True)
    end = serializers.DateTimeField(source='profile.end',read_only=True)
    vip = serializers.BooleanField(source='profile.vip',read_only=True)

    class Meta:
        model = User
        read_only_fields = ('id',
                            'username',
                            'email',
                            'last_login',
                            'date_joined',
                            'is_active',
                            'vip',
                            'last_login_ip',
                            'register_ip',
                            'start',
                            'end')
        fields = ('id',
                'url',
                'username', 
                'email', 
                'last_login',
                'date_joined',
                'is_active',
                'vip',
                'nickname',
                'avatar',
                'description',
                'last_login_ip',
                'register_ip',
                'start',
                'end')

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ('id','username')
        fields = ('id','username')


# fork by django-rest-auth.serializer not all

# Get the UserModel
UserModel = User

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_username_email(self, username, email, password):
        user = None
        if email and password:
            user = self.authenticate(email=email, password=password)

        elif username and password:
            user = self.authenticate(username=username, password=password)

        else:
            msg = ('请输入用户名(或邮箱)和密码')
            raise exceptions.ValidationError(msg)
        # print(user)
        return user

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        user = None

        if email:
            try:
                username = UserModel.objects.get(email__iexact=email).get_username()
            except UserModel.DoesNotExist:
                pass

        if username:
            user = self._validate_username_email(username, '', password)
        # self.authenticate 将不会认证is_active为False的时候，在只填入username时会出现user=None ，这里需要重新根据username获取user对象
        if not user:
            try:
                user = UserModel.objects.filter(username=username).first()
                if not user.check_password(password):
                    msg = '密码错误'
                    raise exceptions.ValidationError(msg)
            except AttributeError:
                pass
        if user:
            if not user.is_active:
                attrs['user'] = user
                attrs['active'] = False
                # msg = ('User account is disabled.')
                # raise exceptions.ValidationError(msg)
                return attrs
        else:
            msg = ('无法登录')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        attrs['active'] = True
        return attrs


class RegisterSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=50,min_length=6,required=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True,style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True,style={'input_type': 'password'})

    def validate_username(self, username):
        repeat_username = UserModel.objects.filter(username__exact=username).exists()
        if username and repeat_username:
            raise serializers.ValidationError(('该用户名已经被注册'))
        return username

    def validate_email(self, email):
        repeat_email = UserModel.objects.filter(email=email).exists()
        if email and repeat_email:
            raise serializers.ValidationError(('该邮箱已被注册'))
        return email

    def validate_password1(self, password):
        if len(password) < 6:
            raise serializers.ValidationError(("密码太短，需大于等于6个字符"))
        return password

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(('确认密码和密码不匹配'))
        return data

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):
        self.cleaned_data = self.get_cleaned_data()
        username = request.data.get('username')
        password = request.data.get('password1')
        email = request.data.get('email')
        user = UserModel.objects.create_user(username=username,password=password,email=email,is_active=False)
        return user

class VerifyRegisterEmailSerializer(serializers.Serializer):
    signature = serializers.CharField()

    username = None

    def validate(self,data):
        signature = data.get('signature',None)
        if not signature:
            raise serializers.ValidationError('请输入有效参数')
        try:
            username = signer.unsign(signature,max_age=600)
            self.username = username
        except (BadSignature,SignatureExpired) as e:
            # print(e)
            raise serializers.ValidationError('签名验证失败')
        return data
    
    def save(self):
        user= UserModel.objects.get(username=self.username)
        if user:
            user.is_active = True
            user.save()
        return user
class ActiveConfirmSerilizer(serializers.Serializer):
    message = serializers.CharField()
    # url = serializers.HyperlinkedIdentityField(view_name='')

class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for send reset e-mail.
    """
    email = serializers.EmailField()

    password_reset_form_class = PasswordResetForm

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)
        return value

    def validate(self,data):
        ''' 检查users是否有效'''
        email = data.get('email')
        users = tuple(self.reset_form.get_users(email))

        if not users:
            raise serializers.ValidationError('用户未激活或邮箱不存在')
            
        return data
    
    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }
        self.reset_form.save(**opts)

class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirm reset 
    """
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)


    set_password_form_class = SetPasswordForm

    def validate(self, attrs):
        self._errors = {}

        # Decode the uidb64 to uid to get User object
        try:
            uid = force_text(uid_decoder(attrs['uid']))
            self.user = UserModel._default_manager.get(pk=uid)
            print(self.user)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})
        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(user=self.user, data=attrs)
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': ['Invalid value']})

        return attrs

    def save(self):
        return self.set_password_form.save()

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    def __init__(self, *args, **kwargs):
        self.old_password_field_enabled = getattr(
            settings, 'OLD_PASSWORD_FIELD_ENABLED', False
        )
        self.logout_on_password_change = getattr(
            settings, 'LOGOUT_ON_PASSWORD_CHANGE', False
        )
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)

        if not self.old_password_field_enabled:
            self.fields.pop('old_password')

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.old_password_field_enabled,
            self.user,
            not self.user.check_password(value)
        )

        if all(invalid_password_conditions):
            err_msg = ('旧密码输入错误，请重试')
            raise serializers.ValidationError(err_msg)
        return value

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        self.set_password_form.save()
        if not self.logout_on_password_change:
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(self.request, self.user)

class JWTSerializer(serializers.Serializer):
    """
    Serializer for JWT authentication.
    """
    message = serializers.CharField(read_only=True)
    token = serializers.CharField()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        user_data = UserSerializer(obj['user'], context=self.context).data
        return user_data

