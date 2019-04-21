
class CommentTargetSerializer(object):

    @staticmethod
    def payload(object):

        model_class = object.__class__

        if model_class.__name__ == 'Comment':
            user = object.user
            data = {
                'user':user.username,
                'content':object.content,
                'nested':object.nested,
                'voted':object.voted
            }
        if model_class.__name__ == 'Post':
            user = object.author
            data = {
                'user':user.username,
                'title':object.title,
                'views':object.views,
                'pinned':object.pinned,
                'highlighted':object.highlighted,
                'voted':object.voted
            }
        return data