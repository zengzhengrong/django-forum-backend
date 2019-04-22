from django.db import models
from model_utils.models import TimeStampedModel
from utils.models_field import DictListField
# Create your models here.


'''
使用字段：

1.name 名称  
4.history 前称 在python中最好以序列结构显示

'''
class Category(TimeStampedModel):
    name = models.CharField(max_length=50,unique=True,blank=True,verbose_name='名称')
    history = DictListField(null=True,blank=True,verbose_name='历史记录')


    class Meta:
        ordering = ['-created']
        verbose_name = "分类"
        verbose_name_plural = "分类"

    def __str__(self):
        return self.name
    
