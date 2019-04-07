from .extensions import bcrypt
from webapp.config import db


tags = db.Table(
    'post_tags',
    db.Column('post_id',db.Integer,db.ForeignKey('post.id')),
    db.Column('tag_id',db.Integer,db.ForeignKey('tag.id'))
    )

class Post(db.Model):
    # __tablename__ = 'your_table_name' 通过该方法可以使用已经存在的表
    id = db.Column(db.Integer(),primary_key = True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime())
    comments = db.relationship(
        'Comment',
        backref = 'post',
        lazy = 'dynamic'
        )
    user_id = db.Column(db.Integer(),db.ForeignKey('user.id'))
    tags = db.relationship(
        'Tag',
        secondary = tags,
        backref = db.backref('posts',lazy='dynamic')
        )
    def __init__(self,title):
        self.title = title
    def __repr__(self):
        return "<Post '{}'>".format(self.title)

class Comment(db.Model):
    # __tablename__ = 'your_table_name' 通过该方法可以使用已经存在的表
    id = db.Column(db.Integer(),primary_key = True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    post_id = db.Column(db.Integer(),db.ForeignKey('post.id'))
    def __repr__(self):
        return "<Comment '{}'>".format(self.text[:15])

class Tag(db.Model):
    # __tablename__ = 'your_table_name' 通过该方法可以使用已经存在的表
    id = db.Column(db.Integer(),primary_key = True)
    title = db.Column(db.String(255))
    def __init__(self,title):
        self.title = title
    def __repr__(self):
        return "<Tag '{}'>".format(self.title)
