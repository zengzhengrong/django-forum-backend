from django.contrib.sessions.models import Session
from django.urls import reverse,resolve
from user import views as user_views
from post import views as post_views
from notification import views as notification_views
from comment import views as comment_views
from category import views as category_views

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
# print(dir (resolve(request.path_info).func.view_class))
# print(request.method)
# class_list = [
#     'UserList',
#     'UserLogList',
#     'UserDetail',
#     'CategoryViewSet',
#     'CommentList',
#     'CommentDetail',
#     'NotificationViewSet',
#     'PostViewSets'
# ]

patch_views_actions = [
    # patch to user module
    user_views.UserList.list.token_required = True
    user_views.UserLogList.list.token_required = True
    user_views.UserDetail.update.token_required = True
    # patch to category module
    category_views.CategoryViewSet.retrieve.token_required = True
    category_views.CategoryViewSet.create.token_required = True
    category_views.CategoryViewSet.update.token_required = True
    category_views.CategoryViewSet.partial_update.token_required = True
    category_views.CategoryViewSet.destroy.token_required = True
    # patch to Comment module
    comment_views.CommentViewSet.create.token_required = True
    comment_views.CommentViewSet.retrieve.token_required = True
    comment_views.CommentViewSet.update.token_required = True
    comment_views.CommentViewSet.partial_update.token_required = True
    comment_views.CommentViewSet.destroy.token_required = True
    # patch to Notification module
    notification_views.NotificationViewSet.list.token_required = True
    notification_views.NotificationViewSet.retrieve.token_required = True
    notification_views.NotificationViewSet.update.token_required = True
    notification_views.NotificationViewSet.partial_update.token_required = True
    notification_views.NotificationViewSet.destroy.token_required = True
    # patch to Post module
    post_views.PostViewSet.create.token_required = True
    post_views.PostViewSet.update.token_required = True
    post_views.PostViewSet.partial_update.token_required = True
    post_views.PostViewSet.destroy.token_required = True

]


def check_token_required(request):
    request_view_class = resolve(request.path_info).func.view_class
    if request_view_class.__name__ in class_list:
        request_view_class.
        auth_request = {
            'GET':[]
        }
        pass


