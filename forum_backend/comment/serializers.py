from rest_framework import serializers
from post.models import Post
from category.models import Category
from comment.models import Comment
from django.contrib.contenttypes.models import ContentType
from utils.serializer_tools import CommentTargetSerializer

class CommentSerializer(serializers.ModelSerializer):
    # commmet_user_url = serializers.HyperlinkedIdentityField(view_name='user:user-detail',
    #                                                         lookup_field='pk')
    description = serializers.SerializerMethodField(help_text='动作描述')
    user_id = serializers.ReadOnlyField(source='user.id')
    user = serializers.ReadOnlyField(source='user.username')
    content_type = serializers.ReadOnlyField(source='content_type.id',help_text='内容类型')
    target = serializers.SerializerMethodField(help_text='评论目标对象数据')
    
    # category = serializers.SlugRelatedField(queryset=Category.objects.all(),
    #                                         slug_field='name',
    #                                         allow_null=True)
    # comments = serializers.SlugRelatedField(many=True,
    #                                         slug_field='content',
    #                                         read_only=True,
    #                                         allow_null=True)
    class Meta:
        model = Comment
        read_only_fields = ('user','created','description')
        fields = '__all__'

    def target_model_class(self,obj):
        content_type = ContentType.objects.get_for_id(obj.content_type.id)
        model_class = content_type.model_class()
        return model_class

    def get_target(self,obj):
        model_class = self.target_model_class(obj)
        target_obj = model_class.objects.get(id=obj.object_id)
        data = CommentTargetSerializer.payload(target_obj)
        return data

    def get_description(self,obj):
        model_class = self.target_model_class(obj)
        if model_class.__name__ == 'Comment':
            message='回复评论'
        if model_class.__name__ == 'Post':
            message='评论帖子'
        return message
