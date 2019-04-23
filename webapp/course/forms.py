from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,RadioField,DateField,SelectField,SelectMultipleField
#from wtforms.fields import core
from wtforms.validators import DataRequired,Length
from .models import Category

class PeopleForm(FlaskForm):
    name = StringField('Name',validators = [DataRequired(),Length(max=255)])
    gender = SelectField(label='Gender', choices= [('male','male'),('female','female')])
    birthday = DateField('Birthday', format='%Y-%m-%d')
    categorys = SelectMultipleField('Categorys',choices=[])



class CourseForm(FlaskForm):
    section = SelectField('section',choices=[("1","1"),("2","2"),("3","3")])
    date = DateField('Date', format='%Y-%m-%d')

class CategoryForm(FlaskForm):
    name = StringField('Name',validators = [DataRequired(),Length(max=255)])
    def validate(self):
        check_validate = super(CategoryForm,self).validate()
        if not check_validate:
            return False
        category = Category.query.filter_by(name =self.name.data).first()
        if category:
            self.name.errors.append("Category with that name already exists ")
            return False
        return True
