from flask_login import AnonymousUserMixin
from webapp.config import db
from webapp.blog.extensions import bcrypt

roles = db.Table(
    'role_users',
    db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
    db.Column('role_id',db.Integer,db.ForeignKey('role.id'))
    )

class User(db.Model):
    # __tablename__ = 'your_table_name' 通过该方法可以使用已经存在的表
    id = db.Column(db.Integer(),primary_key = True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    posts = db.relationship(
        'Post',
        backref = 'user',    #backref 可以使得通过Post.user 属性对User对象进行读取和修改
        lazy = 'dynamic'
        )
    roles = db.relationship(
        'Role',
        secondary = roles,
        backref = db.backref('users',lazy = 'dynamic')
        )
    def __init__(self,username):
        self.username = username
        default = Role.query.filter_by(name = "default").one()
        self.roles.append(default)
    def __repr__(self):
        return "<User '{}'>".format(self.username)
    def set_password(self,password):
        self.password = bcrypt.generate_password_hash(password)
    def check_password(self,password):
        return bcrypt.check_password_hash(self.password,password)
    def is_authenticated(self):
        if isinstance(self,AnonymousUserMixin):
            return False
        else:
            return True
    def is_active(self):
        return True
    def is_anonymous(self):
        if isinstance(self,AnonymousUserMixin):
            return True
        else:
            return False
    def get_id(self):
        return str(self.id)

class Role(db.Model):
    id = db.Column(db.Integer(),primary_key = True)
    name = db.Column(db.String(80),unique = True)
    description = db.Column(db.String(255))
    def __init__(self,name):
        self.name = name
    def __repr_(self):
        return "<Role {}>".format(self.name)
