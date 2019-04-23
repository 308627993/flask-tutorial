from webapp.config import db
from sqlalchemy import Enum

categorys = db.Table(
    'categorys',
    db.Column('category_id',db.Integer,db.ForeignKey('category.id')),
    db.Column('teacher_id',db.Integer,db.ForeignKey('teacher.id')),
    db.Column('student_id',db.Integer,db.ForeignKey('student.id'))
    )

class Single_course(db.Model):
    '''
    一对一课程
    '''
    id = db.Column(db.Integer(),primary_key = True)
    student_id = db.Column(db.Integer(),db.ForeignKey('student.id'))
    teacher_id = db.Column(db.Integer(),db.ForeignKey('teacher.id'))
    section = db.Column(db.String(255))# db.Column(Enum("1", "2","3","4","5","6","7","8" ,name="section_enum", create_type=False))
    date = db.Column(db.Date())
    def __init__(self,date,section):
        self.section = section
        self.date = date
    def __repr__(self):
        return "<Single_course '{}-{}'>".format(self.date,self.section)

class Teacher(db.Model):
    '''老师'''
    id = db.Column(db.Integer(),primary_key = True)
    name = db.Column(db.String(255))
    gender = db.Column(db.String(255))#db.Column(Enum("female", "male", name="gender_enum", create_type=False))
    birthday = db.Column(db.Date())
    single_courses = db.relationship(
        'Single_course',
        backref = 'teacher',
        lazy = 'dynamic'
        )
    categorys = db.relationship(
        'Category',
        secondary = categorys,
        backref = db.backref('teachers',lazy='dynamic')
        )
    def __init__(self,name,gender,birthday):
        self.name = name
        self.gender = gender
        self.birthday = birthday
    def __repr__(self):
        return "<Teacher '{}'>".format(self.name)

class Student(db.Model):
    '''学生'''
    id = db.Column(db.Integer(),primary_key = True)
    name = db.Column(db.String(255))
    gender = db.Column(db.String(255))#db.Column(Enum("female", "male", name="gender_enum", create_type=False))
    birthday = db.Column(db.Date())
    single_courses = db.relationship(
        'Single_course',
        backref = 'student',
        lazy = 'dynamic'
        )
    categorys = db.relationship(
        'Category',
        secondary = categorys,
        backref = db.backref('students',lazy='dynamic')
        )
    def __init__(self,name,gender,birthday):
        self.name = name
        self.gender = gender
        self.birthday = birthday
    def __repr__(self):
        return "<Student '{}'>".format(self.name)

class Category(db.Model):
    '''课程类别'''
    id = db.Column(db.Integer(),primary_key = True)
    name = db.Column(db.String(255),unique = True)
    def __init__(self,name):
        self.name = name
    def __repr__(self):
        return "<Category '{}'>".format(self.name)


























'''
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
'''
