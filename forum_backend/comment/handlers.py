from django.db.models.signals import post_save
from notification.models import Notification
from comment.models import Comment

'''
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
'''
def comment_handler(sender, instance, created, **kwargs):
    print(True)
    if created:
        instance.related_obj
        # print(instance.related_obj.__class__.__name__)
        if instance.related_obj.__class__.__name__ == 'Post':
                message = instance.content
                notificaton = Notification(sender=instance.user,
                        receiver=instance.related_obj.author,
                        verb='comment',
                        action=instance,
                        target=instance.related_obj,
                        message=message
                        )
                notificaton.save()
        if instance.related_obj.__class__.__name__ == 'Comment':
                message = instance.content
                notificaton = Notification(sender=instance.user,
                        receiver=instance.related_obj.user,
                        verb='respond',
                        action=instance,
                        target=instance.related_obj,
                        message=message
                        )
                notificaton.save()

post_save.connect(comment_handler,sender=Comment)