from rest_framework import serializers
from notification.models import Notification
from user.serializers import UserSimpleSerializer
from post.models import Post



def find_post(obj):
    if hasattr(obj,'related_obj'):
        obj = obj.related_obj
        if not obj.__class__.__name__ == 'Post':
            return find_post(obj)
    if isinstance(obj,Post):
        return obj
    raise AttributeError('obj is not a Post instance')

class NotificationSerializer(serializers.ModelSerializer):
    """
    目前通知共有 3 种：
    1. 帖子被评论，帖子作者收到通知，通知模型各字段含义为：
        receiver：帖子作者
        sender：回复者
        target：帖子
        action：新评论
        verb: 'comment'
    2. 帖子的回复被其他人回复，即回复别人的回复，被回复者收到通知：
        receiver：被回复者
        sender：回复者
        target：帖子
        action：新回复
        verb: 'respond'
    3. 回复被点赞：
        receiver：被赞者
        sender：回复者
        target：被赞的回复
        action：被赞的回复所属的帖子
        verb: 'like'
    """
    sender = UserSimpleSerializer()
    post = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    receiver = UserSimpleSerializer()
    
    class Meta:
        model = Notification
        read_only_fields = ('sender','receiver','verb','message','action_content_type','action_object_id','target_content_type','target_object_id')
        fields = '__all__'

    def get_comment(self,obj):

        if self.fields.get('message'):
            print(True)
            del self.fields['message'] # 重复显示，删掉
        print(self.fields)
        print(self.get_fields())
        if obj.verb == 'like':
            # 点赞目标回复的内容
            comment = obj.target
            return {
                'id':comment.id,
                'content': comment.content
                }
        elif obj.verb == 'comment':
            # 被评论内容
            comment = obj.action if obj.action else None
            if not comment:
                return None
            return {
                'id':comment.id,
                'content': comment.content
                }
            
        elif obj.verb == 'respond':
            # 被回复的内容
            comment = obj.action
            return {
                'id':comment.id,
                'content': comment.content
                }

    def get_post(self,obj):
        if obj.verb == 'like':
            # 被赞的回复所在的帖子
            post = obj.action
            return {
                'post_id': post.id,
                'post_title': post.title
            }
        else:
            # 评论或者回复所属的帖子
            post = find_post(obj.target)
            return {
                'post_id': post.id,
                'post_title': post.title
            }