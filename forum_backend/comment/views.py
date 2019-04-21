from rest_framework import generics,permissions
from comment.models import Comment
from comment.serializers import CommentSerializer
from django.contrib.contenttypes.models import ContentType
from post.models import Post
# Create your views here.

class CommentList(generics.ListCreateAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        params = self.request.query_params
        print(params)
        ct_id = params.get('post_id')
        if ct_id:
            q = Comment.objects.filter(id=0).all() # 初始化构建一个空查询集
            ct = ContentType.objects.get_for_model(Post)
            comments = Comment.objects.filter(content_type=ct,object_id=ct_id)
            # 查询集虽然是可迭代对象，但是并非一般序列，没有list.extend()方法，需要用到 | 运算
            for comment in comments:
                sub_comments = comment.sub_comment.all()
                if sub_comments:
                    sub_comments = q | sub_comments
                q = sub_comments
            q = comments | q
            print(len(q))
            print(type(q))
            self.queryset = q
        return self.list(request, *args, **kwargs)


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
