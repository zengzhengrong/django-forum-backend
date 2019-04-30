import os
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

BASE_DIR = getattr(settings,'BASE_DIR')
templates_dir = os.path.join(BASE_DIR, 'templates')
template = os.path.join(BASE_DIR, 'templates/user/register_active_email.html')
print(BASE_DIR)
print(templates_dir)
print(template)

def send_active_email(user,signature):
    '''
    发送注册激活邮箱  
    '''
    context = {'username':user.username,
                'site_name':'django-forum',
                'signature':signature,
                'protocol':'http',
                'domain':'127.0.0.1:8000'}

    msg = render_to_string('user/register_active_email.html',context=context)
    subject = '来自django-forum的注册激活通知'
    from_email = getattr(settings,'DEFAULT_FROM_EMAIL','example@example.com')
    target_email = [user.email]
    send_mail(subject,msg,from_email,target_email)