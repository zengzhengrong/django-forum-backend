from __future__ import unicode_literals
import ast
import json
import re
from datetime import datetime , date
from django.db import models

class TimeJsonEncoder(json.JSONEncoder):
    '''
    解决json.dumps 无法序列化时间的问题
    to str(datetime)
    '''
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

class TimeJsonDecoder(json.JSONDecoder):
    '''
    解决json.loads 无法反序列化时间的问题
    to python datetime object
    '''
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
    
    def decode(self, s, _w=json.decoder.WHITESPACE.match):
        """Return the Python representation of ``s`` (a ``str`` instance
        containing a JSON document).

        """
        obj, end = self.raw_decode(s, idx=_w(s, 0).end())
        end = _w(s, end).end()
        if end != len(s):
            raise JSONDecodeError("Extra data", s, end)

        if isinstance(obj,list):
            for dict_obj in obj:
                self.to_datetime_object(dict_obj)
        else:
            self.to_datetime_object(obj)
        return obj

    def to_datetime_object(self,obj):
        if not hasattr(obj,'items'):
            # obj不是dict类型，则不做处理
            return obj
        for k,w in obj.items():
            if isinstance(w,dict):
                return self.to_datetime_object(obj[k])
            if isinstance(w,str):
                if len(w) == 19:
                    datetime_m = re.match('\d+-\d+-\d+ \d+:\d+:\d+',w)
                    if datetime_m:
                        obj[k] = datetime.strptime(w,'%Y-%m-%d %H:%M:%S')
                if len(w) == 10:
                    date_m = re.match('\d+-\d+-\d+',w)
                    if date_m:
                        obj[k] = datetime.strptime(w,'%Y-%m-%d')

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

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return value
 
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

class DictField(models.TextField):

    description = "Stores a python dict"
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
    def from_db_value(self, value, expression, connection):
        # to dict
        if value is None:
            return value
            
        return json.loads(value)

    def to_python(self, value):
        # to dict
        if value is None:
            return value
        value = super().to_python(self,value)
        return json.loads(value)

    def get_prep_value(self, value):
        # to string
        if value is None:
            return value
        return json.dumps(value,cls=TimeJsonEncoder,ensure_ascii=False)
        
class DictListField(models.TextField):

    description = "Stores a python list with dict"
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
    def from_db_value(self, value, expression, connection):
        # to python dict
        if value is None:
            return value
        # print (value)
        return json.loads(value,cls=TimeJsonDecoder) # 如果在这里用TimeJsonDecoder会导致直接序列化显示是个datetime对象

    def to_python(self, value):
        # to python dict
        value = super().to_python(self,value)
        if not value:
            value = []
 
        if isinstance(value, list):
            return value
        return json.loads(value,cls=TimeJsonDecoder)

    def get_prep_value(self, value):
        # to string
        if value is None:
            return value
        return json.dumps(value,cls=TimeJsonEncoder,ensure_ascii=False)

if __name__ == "__main__":
    data = [{'sd':{'ds':datetime.now(),'sds':{'sdss':datetime.now()}},'123':'321','000':111},{'dsdsd':1321},'213123',3213123]
    dj = json.dumps(data,cls=TimeJsonEncoder)
    print(dj,type(dj))
    djl = json.loads(dj,cls=TimeJsonDecoder)
    print('----------------'*5)
    print(djl)
