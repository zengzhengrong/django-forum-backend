import re
from django.contrib.auth import logout
from django.utils import timezone
from user.models import UserLog
from utils.ip import get_ip_address_from_request
from datetime import timedelta
from django.urls import reverse,resolve


class TokenCookieExpireMiddleware:
    '''
    不存在/过期 token 会删除服务端会话
    Expire Token delete session
    '''
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        token = request.COOKIES.get('token',None)
        response = self.get_response(request)
        if not token:
            logout(request)
        # Code to be executed for each request/response after
        # the view is called.

        return response


class UserLogMiddleware:

    ignore_ip = ['0.0.0.0']
    ignore_paths = ['/admin/jsi18n/','/user/logs/']
    ignore_re_paths = [r'/user/logs/[0-9]+']

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
    
        return self.sandwich_handler(request)

    def sandwich_handler(self,request):
        response = self.ignore_request(request,parent=True)
        if response:
            return response
        response = self.check_current_userlog(request)
        if response:
            return response
        response = self.log_response(request)

        return response

    def ignore_request(self,request,parent=None):
        '''
        用于忽略某些请求，不生成用户日志
        当parent=True ,则当前路径含有在屏蔽列表路径中的任意一部分都不会记录日志
        Ignore some request , do not make logs
        If parent is True , current path contain each partially ignore_path are not make logs
        '''

        if self.ignore_re_paths:
            for re_path in self.ignore_re_paths:
                pattern = re.compile(re_path)
                math = pattern.match(request.path)
                if math:
                    return self.get_response(request)

        if request.path in self.ignore_paths:
            return self.get_response(request)

        if parent is True and request.path != '/':
            for path in self.ignore_paths:
                if request.path in path:
                    return self.get_response(request)

    def get_request_data(self,request):
        if request.GET:
            request_data = request.GET.items()
            request_data = dict(request_data)
        elif request.POST:
            request_data = request.POST.items()
            request_data = dict(request_data)
            if request_data.get('password'):
                request_data['password'] = '********' # 不显示密码
            request_data = request_data
        else:
            request_data = None
        return request_data

    def log_request(self,request):
        log = UserLog()
        ip = get_ip_address_from_request(request)
        log.username = request.user
        log.request_ip = ip
        log.request_path = request.path
        log.request_type = request.method
        log.request_headers = dict(request.headers) # new in django2.2
        log.request_data = self.get_request_data(request)
        log.request_meta = self.serializer_request_meta(request.META)
        return log

    def serializer_request_meta(self,meta):
        for key,word in meta.items():
            if not isinstance(word,str):
                meta[key] = str(word)
        return meta

    def serializer_response_data(self,data):
        # do someting to check vaild
        return data
    
    def check_current_userlog(self,request):
        '''
        10s内：只允许一个相同（用户名，请求ip，请求路径，请求类型）的日志
        如果存在相同日志，则return response
        AnonymousUser 匿名用户因无法确认身份，则跳过检查
        '''
        now = timezone.now()
        last_delta = now - timedelta(seconds=10)

        if request.user.is_anonymous:
            return None
        if request.user:
            filter_data = {
                'username': request.user,
                'request_ip': get_ip_address_from_request(request),
                'request_path': request.path,
                'request_type': request.method,
                'created__gte': last_delta
            }
            current_userlog = UserLog.objects.filter(**filter_data).exists()

            if current_userlog:
                return self.get_response(request)
                
    def response_404_unlog(self,log,response):
        '''
        响应状态码 int:404 不做记录
        '''
        if response.status_code == 404:
            del log # 减少对象引用次数
            return response

    def log_response(self,request):
        # response
        log = self.log_request(request)
        response = self.get_response(request)
        response_404 = self.response_404_unlog(log,response)
        if response_404:
            return response_404
        try:
            data = response.data
        except AttributeError or Exception:
            data = None
        log.username = request.user
        log.response_status_code = response.status_code
        log.response_data = data  if not data else self.serializer_response_data(data)
        log.save()
        return response


