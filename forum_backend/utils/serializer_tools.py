
class CommentTargetSerializer(object):

    @staticmethod
    def payload(object,content_type_id):

        model_class = object.__class__

        if model_class.__name__ == 'Comment':
            user = object.user
            data = {
                'id':object.id,
                'content_type':content_type_id,
                'user':user.username if user else 'None',
                'content':object.content,
                'nested':object.nested,
                'voted':object.voted
            }
        if model_class.__name__ == 'Post':
            user = object.author
            data = {
                'id':object.id,
                'content_type':content_type_id,
                'user':user.username if user else 'None',
                'title':object.title,
                'views':object.views,
                'pinned':object.pinned,
                'highlighted':object.highlighted,
                'voted':object.voted
            }
        return data