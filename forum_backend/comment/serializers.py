from rest_framework import serializers
from post.models import Post
from category.models import Category
from comment.models import Comment
from django.contrib.contenttypes.models import ContentType
from utils.serializer_tools import CommentTargetSerializer
from notification.serializers import find_post

class CommentSerializer(serializers.ModelSerializer):
    # commmet_user_url = serializers.HyperlinkedIdentityField(view_name='user:user-detail',
    #                                                         lookup_field='pk')
    description = serializers.SerializerMethodField(help_text='动作描述')
    user_id = serializers.ReadOnlyField(source='user.id')
    user = serializers.ReadOnlyField(source='user.username')
    content_type_id = serializers.ReadOnlyField(source='content_type.id',help_text='内容类型')
    target = serializers.SerializerMethodField(help_text='评论目标对象数据')
    relay_source = serializers.SerializerMethodField(help_text='转发源')
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

    def get_relay_source(self,obj):
        from_object = self._context.get('request').data.get('from_object') # POST 请求所响应需要显示评论的转发
        if from_object:
            print(from_object)
        # GET request will be processing for below
        relay_data = obj.relay_source
        if relay_data:
            relay_type ,relay_id = relay_data.get('type'),relay_data.get('id')
            # if the model type is no Post or Comment model return None
            if relay_type not in ['Post','Comment']:
                return None
            if relay_type == 'Post':
                post = Post.objects.filter(id=relay_id).first()
                serializer = RelayPostSerializer(post,context={'request': self._context.get('request')})
                return serializer.data
            if relay_type == 'Comment':
                comment = Comment.objects.filter(id=relay_id).first()
                serializer = RelayCommentSerializer(comment)
                return serializer.data

        return None


class RelayPostSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='post:post-detail')
    author = serializers.ReadOnlyField(source='author.username',allow_null=True)

    class Meta:
        model = Post
        fields = ['id','url','author','category','title','body','created']


class RelayCommentSerializer(serializers.ModelSerializer):

    # url = serializers.HyperlinkedIdentityField(view_name='post:post-detail')
    user = serializers.ReadOnlyField(source='user.username',allow_null=True)
    post = serializers.SerializerMethodField(help_text='所属帖子')

    class Meta:
        model = Comment
        fields = ['id','user','post','body','created']

    def get_post(self,obj):
        print (obj)
        post = find_post(obj)
        return None




