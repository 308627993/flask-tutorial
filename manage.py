import os
from flask_script import Manager,Server
from flask_migrate import  MigrateCommand

from webapp import create_app
from webapp.config import db
from webapp.auth.models import *
from webapp.blog.models import *
from webapp.course.models import *

env = os.environ.get('WEBAPP_ENV','dev')
app = create_app('webapp.config.%sConfig'%env.capitalize())
manager = Manager(app)
manager.add_command('server',Server())
manager.add_command('db',MigrateCommand)



@manager.shell
def make_shell_context():
    return dict(app=app,db=db,User=User,Post=Post,Comment=Comment,Tag=Tag,Role=Role,Teacher=Teacher,Student=Student,Single_course=Single_course,Category=Category)

if __name__ == '__main__':
    manager.run()
