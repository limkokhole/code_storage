from models import Model
from models.user import User


# 微博类
class Weibo(Model):
    @classmethod
    def update(cls, id, form):
        w = cls.find(id)
        valid_names = [
            'content'
        ]
        for key in form:
            # 这里只应该更新我们想要更新的东西
            if key in valid_names:
                # w.key = form[key]
                setattr(w, key, form[key])
        w.save()
        return w

    def __init__(self, form):
        self.id = None
        self.content = form.get('content', '')

    def json(self):
        d = self.__dict__.copy()
        comments = [c.json() for c in self.comments()]
        d['comments'] = comments
        return d

    def comments(self):
        return Comment.find_all(weibo_id=self.id)


# 评论类
class Comment(Model):
    def __init__(self, form):
        self.id = None
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.weibo_id = int(form.get('weibo_id', -1))
