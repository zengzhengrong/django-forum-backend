from django.db import models
from model_utils.models import TimeStampedModel,SoftDeletableModel
from django.conf import settings
from model_utils.models import StatusModel
from model_utils import Choices
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.

class Notification(TimeStampedModel,StatusModel,SoftDeletableModel):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='notifications_sender',on_delete=models.SET_NULL,null=True,verbose_name='发送者')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='notifications_receiver',on_delete=models.SET_NULL,null=True,verbose_name='接收者')
    STATUS = Choices('unread','read')
    message = models.TextField(blank=True,verbose_name='消息内容')
    verb =  models.CharField(max_length=50,null=True,blank=True,verbose_name='动词')
    action_content_type = models.ForeignKey(ContentType,blank=True,null=True,related_name='notifications_action',on_delete=models.CASCADE,verbose_name='关联动作类型')
    action_object_id = models.PositiveIntegerField(blank=True,null=True,verbose_name='关联动作类型ID')
    action = GenericForeignKey('action_content_type','action_object_id')

    target_content_type = models.ForeignKey(ContentType,blank=True,null=True,related_name='notifications_target',on_delete=models.CASCADE,verbose_name='关联目标类型')
    target_object_id = models.PositiveIntegerField(blank=True,null=True,verbose_name='关联目标类型ID')
    target = GenericForeignKey('target_content_type','target_object_id')

    class Meta:

        ordering = ['-created']
        verbose_name = "通知"
        verbose_name_plural = "通知"

    def __str__(self):
        return self.sender.username



