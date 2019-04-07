from flask import render_template,Blueprint,redirect,url_for,flash,request
from .forms import LoginForm,RegisterForm
from .models import User,db
from flask_login import login_user,logout_user
from flask_principal import Identity,AnonymousIdentity,identity_changed,current_app

main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder = './templates/auth'
    )

@main_blueprint.route('/')
def index():
    return redirect(url_for('blog.home',page=1))

@main_blueprint.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).one()
        login_user(user,remember = form.remember.data)
        print('next--------------------------------------:',(request.args.get('next')))
        next = request.args.get('next')
        identity_changed.send(current_app._get_current_object(),identity = Identity(user.id))
        #flash('You have been logged in .',category='success')

        #if not next_is_valid(next):
        #    return flask.abort(400)
        return redirect(next or url_for('blog.home',page=1))
    return render_template('login.html',form=form)

@main_blueprint.route('/logout',methods=['GET','POST'])
def logout():
    logout_user()
    identity_changed.send(current_app._get_current_object(),identity = AnonymousIdentity())
    #flash('You have been logged in .',category='success')
    return redirect(url_for('.login'))

@main_blueprint.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(form.username.data)
        #new_user.username = form.username.data
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Your user has been created,please login .',category='success')
        return redirect(url_for('.login'))
    return render_template('register.html',form=form)
