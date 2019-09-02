
from functools import wraps
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from utils.jwt import jwt_decode

'''
列出需要用户认证的请求（除了登出）*号表示需要admin认证：
1.*获取后端所有用户-UserList
2.*获取后端所有用户日志-UserLogList
3.修改自身用户信息-UserDetail.put
4.*获取后端分类模型详情及相关操作-CategoryViewSet.get:retrieve.post.put.patch.delete
5.发布评论-CommentList.post
6.*RUD评论-CommentDetail.get:retrieve.put.patch.delete
7.获取用户自身所收到的所有通知-NotificationViewSet.get:(list,retrieve).put.patch.delete
8.发表修改删除文章-PostViewSets.post.put.patch.delete
'''


def token_required(f):
    '''
    需要身份验证的请求
    用于生成类方法装饰器
    postman 中选择在请求头添加Authorization，值为token
    '''
    @wraps(f)
    def decorated(request,*args,**kwargs):
        auth_token = request.headers.get('Authorization')

        if not auth_token: # 无token
            return Response({'message':'Provide token'},403)
        
        username,status_code = jwt_decode(auth_token)

        if status_code == 200: # token 验证通过，匹配后端session的user数据
            if request.user.username == username:
                return f(request,*args,**kwargs) # 身份验证通过返回方法
            return Response({'message':'Session Invalid'},403) # session 验证错误

        if status_code == 403: # token 验证不通过
            return Response({'message':'Invalid token'},403)

        return f(request,*args,**kwargs)
    return decorated