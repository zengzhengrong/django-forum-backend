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


class ListPostSerializer(serializers.Serializer):
    '''
    search:搜索词,可以根据前缀符号来限制搜索，如'^title' 匹配开头，默认是模糊搜索
    ordering:排序 ，支持的栏位(views, created, highlighted) or (-views, -created, -highlighted) -符表示倒序
    page:页数
    page_size:一页的个数
    category_id:分类的id，只获取该分类下的帖子
    lt_datetime:只获取小于该时间的帖子，格式：%Y-%m-%dT%H:%M:%S
    '''
    category_id = serializers.IntegerField(help_text='分类的id，只获取该分类下的帖子',required=False)
    lt_datetime = serializers.DateTimeField(help_text='只获取小于该时间的帖子，格式：%Y-%m-%dT%H:%M:%S',required=False)
    # search = serializers.CharField(help_text='搜索词,可以根据前缀符号来限制搜索，如^title 匹配开头，默认是模糊搜索')
    # ordering = serializers.ChoiceField(choices=('views', 'created', 'highlighted','-views', '-created', '-highlighted'),
    #                                 help_text='排序 ，支持的栏位(views, created, highlighted) or (-views, -created, -highlighted) -符表示倒序')

    # page = serializers.IntegerField(help_text='指定页数')
    # page_size = serializers.IntegerField(help_text='一页的个数')