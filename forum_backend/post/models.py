from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from model_utils.models import TimeStampedModel
from comment.models import Comment
from category.models import Category
from utils.models_field import ListField
# Create your models here.


'''
Post

1.author 外键指向User  
2.category 外键指向Category  
3.title 标题  
4.body 内容  
5.is_vote 是否为发起投票的post  
6.created_time 创建时间  
7.updated_time 更新时间 
8.pinned 置顶
9.highlighted 高亮/加精
10. hidden 隐藏
11.views 浏览量
'''

class Post(TimeStampedModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='posts',on_delete=models.SET_NULL,null=True,verbose_name='作者')
    category = models.ForeignKey(Category,related_name='posts',on_delete=models.SET_NULL,null=True,verbose_name='分类')
    title = models.CharField(max_length=128,verbose_name='标题')
    body = models.TextField(blank=True,verbose_name='正文')
    views = models.PositiveIntegerField(default=0, editable=False,verbose_name='浏览量')
    pinned = models.BooleanField(default=False,verbose_name='置顶性质')
    highlighted = models.BooleanField(default=False,verbose_name='加精性质')
    hidden = models.BooleanField(default=False,verbose_name='隐藏性质')
    voted = models.BooleanField(default=False,verbose_name='投票性质')
    comments = GenericRelation(Comment,content_type_field='content_type',object_id_field='object_id',verbose_name='评论')


    
    class Meta:
        ordering = ['-created']
        verbose_name = "帖子"
        verbose_name_plural = "帖子"
    
    def add_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return f'<Post:{self.title}>'

'''
Vote

1.post 关联post外键指向post 一对一
2.user 关联django user 外键
3.question 问题
4.created_time
'''

class Vote(TimeStampedModel):
    post = models.OneToOneField(Post,related_name='vote',on_delete=models.SET_NULL,null=True,verbose_name='关联帖子')
    promoter = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='votes',on_delete=models.SET_NULL,null=True,verbose_name='发起人')
    question = models.CharField(max_length=100, blank=True, null=True, verbose_name='投票问题')
    options = ListField(blank=True, null=True,verbose_name='选项')
    voters = GenericRelation(Comment,content_type_field='content_type',object_id_field='object_id',verbose_name='投票者')

    class Meta:
        ordering = ['-created']
        verbose_name = "投票"
        verbose_name_plural = "投票"

    def __str__(self):
        return f'<Vote:{self.question}>'


