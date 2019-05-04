from rest_framework import serializers
from post.models import Post
from category.models import Category
from comment.models import Comment

class PostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='post:post-detail')
    author = serializers.ReadOnlyField(source='author.username',allow_null=True)
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='name',
                                            allow_null=True)
    # comments = serializers.SlugRelatedField(many=True,
    #                                         slug_field='content',
    #                                         read_only=True,
    #                                         allow_null=True)
    class Meta:
        model = Post
        read_only_fields = ('views','pinned','highlighted','hidden','comments','created')
        fields = '__all__'