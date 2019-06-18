from rest_framework import serializers
from post.models import Post
from category.models import Category

class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='category:category-detail')
    history = serializers.SerializerMethodField(allow_null=True)
    
    class Meta:
        model = Category
        read_only_fields = ('id','history')
        fields = '__all__'

    def get_history(self,obj):
        if obj.history is None:
            return None

        # history_list = []

        # for i in obj.history:
        #     history = History(i['name'],i['updated'])
        #     history_list.append(history)
            
        serializer = CategoryHistorySerializer(obj.history,many=True)
        return serializer.data

class History:

    def __init__(self,name,updated):
        self.name = name
        self.updated = updated

class CategoryHistorySerializer(serializers.Serializer):
    name = serializers.CharField()
    updated = serializers.DateTimeField()