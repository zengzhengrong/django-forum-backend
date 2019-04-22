from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()
class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        read_only_fields = ('user','vip','last_login_ip','register_ip','start','end')
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user:user-detail'),
    profile = serializers.SerializerMethodField()


    class Meta:
        model = User
        read_only_fields = ('url','username', 'email','last_login' ,'date_joined', 'is_active')
        fields = ('url','username', 'email', 'profile','last_login' ,'date_joined', 'is_active')

    def get_profile(self,object):

        profile = object.profile
        if profile:
            return UserProfileSerializer(profile).data 
        return {'status':'500','message':'get user profile error'}


