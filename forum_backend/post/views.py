from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from post.serializers import PostSerializer
from post.permissions import IsPostAuthorOrReadOnly
from post.models import Post
# Create your views here.



class PostViewSets(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsPostAuthorOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

