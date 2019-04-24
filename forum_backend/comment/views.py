from rest_framework import generics,permissions
from comment.models import Comment
from comment.serializers import CommentSerializer
from django.contrib.contenttypes.models import ContentType
from post.models import Post
from rest_framework.response import Response
from rest_framework import status
from . import handlers
# Create your views here.

def get_total(comments):

    has_sub = has_subcomments(comments)

    if True not in has_sub:
        total = comments
    else:
        q = Comment.objects.filter(id=0).all() # 初始化构建一个空查询集
        total = get_subcomments(comments,q=q)

    return total
def has_subcomments(comments):
    total = []
    for c in comments:
        sub = c.sub_comment.all()
        if not sub:
            sub = False
            total.append(sub)
        else:
            sub = True
            total.append(sub)
    return total

def get_subcomments(comments,total=None,q=None):
    '''
    查询集虽然是可迭代对象，但是并非一般序列，没有list.extend()方法，需要用到 | 运算
    '''
    total_copy = total

    for comment in comments:
        sub_comments = comment.sub_comment.all()
        if not sub_comments:
            continue
        if sub_comments:
            sub_comments = q | sub_comments # 
        q = sub_comments
        if total is not None:
            total = total | q
            # print(total)
        else:
            total = comments | q
            # print(total)
    if total_copy == total:
        return total
    q = Comment.objects.filter(id=0).all() # 初始化构建一个空查询集
    return get_subcomments(sub_comments,total=total,q=q)



class CommentList(generics.ListCreateAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        params = self.request.query_params
        # print(params)
        ct_id = params.get('post_id')
        if ct_id:
            ct = ContentType.objects.get_for_model(Post)
            comments = Comment.objects.filter(content_type=ct,object_id=ct_id)
            total = get_total(comments)
            print(len(total))
            print(type(total))
            self.queryset = total
        return self.list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)





class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAdminUser,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        data = {
            'message':'成功删除评论'
        }
        return Response(data,status=status.HTTP_204_NO_CONTENT)
