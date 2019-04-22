import ast
from django.db import models
 
class ListField(models.TextField):
    '''
    用于将数据库的值转换为python的list对象
    to_python:将from_db_value返回的数据库的字符转换为python的list对象  
    get_prep_value：将python对象转换为查询值  
    value_to_string：支持序列化，返回字符串

    '''
    description = "Stores a python list"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
    def to_python(self, value):
        if not value:
            value = []
 
        if isinstance(value, list):
            return value
 
        return ast.literal_eval(value)
 
    def get_prep_value(self, value):
        if value is None:
            return value
 
        return str(value)
 
    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_db_prep_value(value)


class DictListField(ListField):

    description = "Stores a python list with dict"
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
     
    def to_python(self, value):
        value = super().to_python(self,value)
        if not value:
            value = []
 
        if isinstance(value, list):
            return value
 
        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        print(value)
        print(type(value))
        for item in value:
            if not isinstance(item,dict):
                raise TypeError('The Field must be a list nesting in dict')

        return str(value)
