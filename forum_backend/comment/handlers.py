from django.db.models.signals import post_save
from notification.models import Notification
from comment.models import Comment
from django.conf import settings
from django.contrib.auth import get_user_model
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
4.可以选择收到所有回复
在settings中设定AUTH_USER_ADMINS，不设置即不通知管理员
verb: 'like'
'''
User = get_user_model()



def get_admins():
	admins = getattr(settings,'AUTH_USER_ADMINS',None)
	if admins:
		if not isinstance(admins,list):
			return TypeError('AUTH_USER_ADMINS must be a list ')
		admins = User.objects.filter(username__in=admins).all()	
		return admins
	return None

admins = get_admins()

def comment_handler(sender, instance, created, **kwargs):
	if created:
		if instance.related_obj.__class__.__name__ == 'Post':
			verb = 'comment'
			if instance.user != instance.related_obj.author:
				message = instance.content
				notificaton = Notification(sender=instance.user,
						receiver=instance.related_obj.author,
						verb=verb,
						action=instance,
						target=instance.related_obj,
						message=message,
						description='评论了'
						)
				notificaton.save()

		if instance.related_obj.__class__.__name__ == 'Comment':
			verb = 'respond'
			if instance.user != instance.related_obj.user:
				message = instance.content
				notificaton = Notification(sender=instance.user,
						receiver=instance.related_obj.user,
						verb=verb,
						action=instance,
						target=instance.related_obj,
						message=message,
						description='回复了'
						)
				notificaton.save()

		if instance.user not in admins:
			if instance.related_obj.__class__.__name__ == 'Post':
				if instance.related_obj.author in admins: # 避免发帖者同时又是管理员时候重复接收不同类型的通知
					return None
			if instance.related_obj.__class__.__name__ == 'Comment':
				if instance.related_obj.user in admins: # 避免被回复者同时又是管理员时候重复接收不同类型的通知
					return None
			for admin in admins:
				message = instance.content
				notificaton = Notification(sender=instance.user,
										receiver=admin,
										verb=verb,
										action=instance,
										target=instance.related_obj,
										message=message,
										description='通知给管理员'
										)
				notificaton.save()



post_save.connect(comment_handler,sender=Comment)