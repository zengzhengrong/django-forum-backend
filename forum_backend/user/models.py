from django.db import models
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from model_utils.models import TimeFramedModel,TimeStampedModel
from model_utils import Choices
from django.conf import settings
from utils.ip import get_ip_address_from_request
from utils.models_field import DictField
from django.contrib.auth.signals import user_logged_in
# Create your models here.
'''
单独一个profile表来扩展用户

使用字段


1.user 外键指向 django User
2.nickname 昵称  
3.avatar 头像  
4.description 自我描述  
5.last_login_ip 最后一次登录IP
6.register_ip 注册时候IP
'''


class UserProfile(TimeFramedModel,TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,related_name='profile',on_delete=models.SET_NULL,null=True,verbose_name='用户')
    nickname = models.CharField(max_length=50, blank=True,null=True,verbose_name='昵称')
    avatar = ProcessedImageField(upload_to='avatar',
                                 default='avatar/default.png', 
                                 processors=[ResizeToFill(85,85)],
                                 verbose_name='头像'
                                 )
    description = models.CharField(max_length=150,null=True,blank=True,verbose_name='自我描述')
    vip = models.BooleanField(default=False,verbose_name='VIP会员性质')
    last_login_ip = models.GenericIPAddressField(unpack_ipv4=True,blank=True,null=True,verbose_name='最近一次登陆IP')
    register_ip = models.GenericIPAddressField(unpack_ipv4=True, blank=True, null=True,verbose_name='注册IP')



    class Meta:
        verbose_name = "用户配置"
        verbose_name_plural = "用户配置"
        ordering = ['-created']

    def __str__(self):
        return self.user.username if self.user else 'None'


class UserLog(TimeStampedModel):
    username = models.CharField(max_length=150,null=True,blank=True,verbose_name='所属用户名')
    request_ip = models.GenericIPAddressField(unpack_ipv4=True, blank=True, null=True,verbose_name='请求IP')
    request_path = models.CharField(max_length=150,null=True,blank=True,verbose_name='请求路径')
    http_type = Choices('GET','POST','DELETE','PUT','PATH')
    request_type = models.CharField(choices=http_type,max_length=10,null=True,blank=True,verbose_name='请求类型')
    request_data = DictField(null=True,blank=True,verbose_name='请求数据')
    request_meta = DictField(null=True,blank=True,verbose_name='请求元数据')
    response_status_code = models.CharField(max_length=10,null=True,blank=True,verbose_name='响应状态码')
    response_data = DictField(null=True,blank=True,verbose_name='响应数据')

    class Meta:
        verbose_name = "用户日志"
        verbose_name_plural = "用户日志"
        ordering = ['-created']
    
    def __str__(self):
        return f'<Userlog:{self.username},{self.request_type}>'


def create_userprofile_or_update_last_ip(sender, user, request, **kwargs):
    """
    登陆进来时创建用户配置或者更新登陆ip
    """
    ip = get_ip_address_from_request(request)
    profile, first = UserProfile.objects.get_or_create(user=user)
    if first:
        profile.register_ip = ip
        profile.last_login_ip = ip
    if not first:
        profile.last_login_ip = ip
    profile.save()



user_logged_in.connect(create_userprofile_or_update_last_ip)
