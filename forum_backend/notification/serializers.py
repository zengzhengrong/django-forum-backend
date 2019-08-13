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
    1. 帖子被评论，帖子作者收到通知
    2. 帖子的回复被其他人回复，即回复别人的回复，被回复者收到通知
    3. 回复被点赞
    4. 管理员收到所有关于评论通知
    """
    # reply_comment replied_comment 

    sender = UserSimpleSerializer()
    post = serializers.SerializerMethodField()
    reply_comment = serializers.SerializerMethodField() # 评论
    replied_comment = serializers.SerializerMethodField() # 被回复的评论
    receiver = UserSimpleSerializer()
    
    class Meta:
        model = Notification
        read_only_fields = ('sender','receiver','verb','action_content_type','action_object_id','target_content_type','target_object_id')
        # fields = '__all__'
        exclude = ['message']

    def get_reply_comment(self,obj):
        
        if obj.verb == 'like':
            # 点赞目标回复的内容
            comment = obj.target
            return {
                'id':comment.id,
                'content': comment.content
                }
        elif obj.verb == 'comment':
            # 评论内容 面向post
            comment = obj.action if obj.action else None
            if not comment:
                return None
            return {
                'id':comment.id,
                'content': comment.content
                }
            
        elif obj.verb == 'respond':
            # 回复的内容 面向comment
            comment = obj.action
            return {
                'id':comment.id,
                'content': comment.content
                }

    def get_replied_comment(self,obj):
        
        if obj.verb == 'respond':
            replied_comment = obj.target

            if replied_comment:
                return {
                    'id':replied_comment.id,
                    'content':replied_comment.content
                    }
        return None

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


