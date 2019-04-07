from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Length,EqualTo,URL
from .models import User


class LoginForm(FlaskForm):
    username = StringField('Username',validators = [DataRequired(),Length(max=255)])
    password = PasswordField('Password',validators = [DataRequired()])
    remember = BooleanField("Remember Me")
    def validate(self):
        check_validate = super(LoginForm,self).validate()
        if not check_validate:
            return False
        user = User.query.filter_by(username = self.username.data).first()
        if not user:
            self.username.errors.append('Invalid username or password')
            return False
        if not user.check_password(self.password.data):
            return False
        return True

class RegisterForm(FlaskForm):
    username = StringField('Username',validators = [DataRequired(),Length(max=255)])
    password = PasswordField('Password',validators = [DataRequired(),Length(min=8)])
    confirm = PasswordField('Confirm Password',validators = [DataRequired(),EqualTo('password')])
    def validate(self):
        check_validate = super(RegisterForm,self).validate()
        if not check_validate:
            return False
        user = User.query.filter_by(username =self.username.data).first()
        if user:
            self.username.errors.append("User with that name already exists ")
            return False
        return True
