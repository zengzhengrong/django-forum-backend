from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.conf import settings
from utils.models_field import DictField
# Create your models here.

'''
使用django 的ContentType来构建外键实现回复以及内联回复和投票，减少创建多个表

使用字段

1.user 外键指向User  
2.post 外键指向Post  
3.content 评论内容  
4.content_type 外键指向Django的ContentType  
5.object_id 表示content_type的模型ID  
6.related_obj 根据content_type和content_type_id生成通用外键  
7.is_comment_nested 是否为评论内联  
8.is_comment_vote 是否为投票  
9.created_time 创建时间  
'''
# models.ForeignKey(ContentType,blank=True,null=True,related_name='ct_action',verbose_name='动作类型',on_delete=models.CASCADE)

class Comment(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='comments',on_delete=models.SET_NULL,null=True,verbose_name='评论人')
    content = models.TextField(blank=True,verbose_name='内容')
    content_type = models.ForeignKey(ContentType,blank=True,null=True,related_name='comments',on_delete=models.CASCADE,verbose_name='关联类型')
    object_id = models.PositiveIntegerField(blank=True,null=True,verbose_name='关联类型ID')
    related_obj = GenericForeignKey('content_type','object_id')
    nested = models.BooleanField(default=False,verbose_name='评论内联性质')
    voted = models.BooleanField(default=False,verbose_name='投票性质')
    sub_comment = GenericRelation('Comment',content_type_field='content_type',object_id_field='object_id',verbose_name='子评论')
    relay_source = DictField(blank=True,null=True,verbose_name='转发源')
    
    class Meta:
        
        ordering = ['-created']
        verbose_name = "评论/回复/投票"
        verbose_name_plural = "评论/回复/投票"

    def __str__(self):
        return self.user.username if self.user else 'None'
