from rest_framework import serializers
from post.models import Post
from category.models import Category

class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='category:category-detail')

    class Meta:
        model = Category
        read_only_fields = ('id','history')
        fields = '__all__'