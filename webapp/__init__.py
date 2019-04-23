from flask import Flask,redirect,url_for
from flask_principal import identity_loaded,UserNeed,RoleNeed
from flask_login import current_user

from webapp.config import DevConfig,db,migrate
from webapp.blog.views import blog_blueprint
from webapp.auth.views import main_blueprint
from webapp.course.views import course_blueprint
from webapp.auth.extensions import login_manager,principals
from webapp.blog.extensions import bcrypt
from webapp.course.api import course_api





def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    db.init_app(app)
    migrate.init_app(app,db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    principals.init_app(app)
    course_api.init_app(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender,identity):
        #set the identity user object
        identity.user = current_user
        #add the userneed to the identity
        if hasattr(current_user,'id'):
            identity.provides.add(UserNeed(current_user.id))
        #add each role to the identity
        if hasattr(current_user,'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))
    '''
    @app.route('/')
    def index():
        return redirect(url_for('blog.home',page=1))
    '''
    app.register_blueprint(blog_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(course_blueprint)
    return app
