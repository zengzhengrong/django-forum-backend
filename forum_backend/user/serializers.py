from rest_framework import serializers,exceptions
from .models import UserProfile
from django.contrib.auth import get_user_model
from django.contrib.auth import login,logout,authenticate
from django.utils.translation import ugettext_lazy as _
User = get_user_model()

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


# fork by django-rest-auth

# Get the UserModel
UserModel = User

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_username(self, username, password):
        user = None

        if username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _('Must include "username" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username_email(self, username, email, password):
        user = None

        if email and password:
            user = self.authenticate(email=email, password=password)
        elif username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _('Must include either "username" or "email" and "password".')
            raise exceptions.ValidationError(msg)

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

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs


class JWTSerializer(serializers.Serializer):
    """
    Serializer for JWT authentication.
    """
    token = serializers.CharField()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        """
        Required to allow using custom USER_DETAILS_SERIALIZER in
        JWTSerializer. Defining it here to avoid circular imports
        """
        user_data = UserSerializer(obj['user'], context=self.context).data
        return user_data

