from app import db, marshmallow
from flask import jsonify

from marshmallow import fields


class Sub(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(300))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    @classmethod
    def create_sub(cls, name, description):
        new_sub = Sub(name, description)
        try:
            db.session.add(new_sub)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        return sub_schema.jsonify(new_sub)

    @classmethod
    def get_sub(cls, subid):
        sub = Sub.query.get(subid)
        return sub_schema.jsonify(sub)

    @classmethod
    def get_subs(cls):
        subs = Sub.query.all()
        return subs_schema.jsonify(subs)


class SubSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'name', 'description')


sub_schema = SubSchema()
subs_schema = SubSchema(many=True,)


class Post(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime())
    user = db.Column(db.String(100))
    title = db.Column(db.String(200))
    text = db.Column(db.String(500))
    sub = db.Column(db.Integer, db.ForeignKey("sub.id"))

    def __init__(self, user, title, text, sub):
        self.user = user
        self.title = title
        self.text = text
        self.sub = sub

    @classmethod
    def create_post(cls, user, title, text, sub):
        new_post = Post(user, title, text, sub)
        try:
            db.session.add(new_post)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        return post_schema.jsonify(new_post)

    @classmethod
    def get_post(cls, postid):
        post = Post.query.get(postid)
        # sub = Sub.query.get(post.sub)
        # post.sub = sub
        return post_schema.jsonify(post)

    @classmethod
    def get_posts(cls):
        posts = Post.query.all()
        return posts_schema.jsonify(posts)

    @classmethod
    def delete_post(cls, post_id):
        post = Post.query.get(post_id)
        db.session.delete(post)
        db.session.commit()
        return post_schema.jsonify(post)

    @classmethod
    def update_post(cls, post_id, title=None, text=None, user=None, sub=None):
        post = Post.query.get(post_id)
        if title != None:
            post.title = title
        if text != None:
            post.text = text
        if user != None:
            post.user = user
        db.session.commit()
        return post_schema.jsonify(post)


class PostSchema(marshmallow.Schema):
    # sub = fields.Nested(sub_schema)

    class Meta:
        fields = ('id', 'user', 'title', 'text', 'sub')


# Init Schema
post_schema = PostSchema()
posts_schema = PostSchema(many=True)


class Comment(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(300))
    post = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)

    def __init__(self, title, description, post):
        self.title = title
        self.description = description
        self.post = post

    @classmethod
    def create_comment(cls, title, description, post):
        new_comment = Comment(title, description, post)
        try:
            db.session.add(new_comment)
            db.session.commit()
        except:
            db.session.rollback()
            raise

        return comment_schema.jsonify(new_comment)

    @classmethod
    def get_comment(cls, commentid):
        comment = Comment.query.get(commentid)
        return comment_schema.jsonify(comment)

    @classmethod
    def get_comments(cls):
        comments = Comment.query.all()
        return comments_schema.jsonify(comments)

    @classmethod
    def update_comment(cls, comment_id, title=None, description=None):
        comment = Comment.query.get(comment_id)
        if title != None:
            comment.title = title
        if description != None:
            comment.description = description
        db.session.commit()
        return comment_schema.jsonify(comment)

    @classmethod
    def delete_comment(cls, comment_id):
        comment = Comment.query.get(comment_id)
        db.session.delete(comment)
        db.session.commit()
        return comment_schema.jsonify(comment)


class CommentSchema(marshmallow.Schema):
    class Meta:
        fields = ('title', 'description', 'post')


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)

if __name__ == 'models':
    db.create_all()
