import datetime,calendar
from sqlalchemy import func,text,extract
from flask import render_template,Blueprint,redirect,url_for,abort
from webapp.config import db
from .models import *
from webapp.auth.models import User
from .forms import *
from flask_login import login_required,current_user
from webapp.auth.extensions import poster_permission,admin_permission
from flask_principal import Permission,UserNeed
from itertools import groupby

course_blueprint = Blueprint(
    'course',
    __name__,
    template_folder = './templates/',
    url_prefix = '/course'
    )
@course_blueprint.route('/',methods=('GET','POST'))
def home():
    return render_template('course/home.html')

@course_blueprint.route('/new/<string:item>',methods=('GET','POST'))
def new(item):
    if item == 'category':
        form = CategoryForm()
        if form.validate_on_submit():
            new_category = Category(form.name.data)
            db.session.add(new_category)
            db.session.commit()
            return redirect(url_for('.home'))
        return render_template('course/new_category.html',form = form)
    elif item == 'teacher':
        form = PeopleForm()
        if form.validate_on_submit():
            new_teacher = Teacher(form.name.data,form.gender.data,form.birthday.data)
            db.session.add(new_teacher)
            db.session.commit()
            return redirect(url_for('.home'))
        return render_template('course/new_people.html',form = form,item='teacher')
    elif item == 'student':
        form = PeopleForm()
        if form.validate_on_submit():
            new_student = Student(form.name.data,form.gender.data,form.birthday.data)
            db.session.add(new_student)
            db.session.commit()
            return redirect(url_for('.home'))
        return render_template('course/new_people.html',form = form,item='student')
    elif item == 'course':
        form = CourseForm()
        if form.validate_on_submit():
            new_course = Single_course(form.date.data,form.section.data)
            db.session.add(new_course)
            db.session.commit()
            return redirect(url_for('.home'))
        return render_template('course/new_course.html',form = form)

class WorkoutCalendar(calendar.HTMLCalendar):
    def __init__(self, workouts):
        super(WorkoutCalendar, self).__init__()
        self.firstweekday=7
        self.workouts = self.group_by_day(workouts)

    def formatday(self, day, weekday):
        body=[]
        if day != 0:
            sections = []
            cssclass = self.cssclasses[weekday]
            if datetime.date.today() == datetime.date(int(self.year), int(self.month), int(day)):
                cssclass += ' today'
            if day in self.workouts:
                sections = [workout.section for workout in  self.workouts[(day)]] # which day which section list
                print("sections",sections)
                for i in range(1,10):
                    if str(i) in sections:
                        body.append("<div id=%s-%s-%s-%s class='btn btn-success' >%s</div>"%(self.year,self.month,str(day),i,i))
                    else:
                        body.append("<div id=%s-%s-%s-%s class='btn btn-outline-dark' onclick='change_status(this)'>%s</div>"%(self.year,self.month,str(day),i,i))
                return self.day_cell(cssclass, '%s' % (''.join(body)))
            for i in range(1,10):
                body.append("<div id=%s-%s-%s-%s class='btn btn-outline-dark' onclick='change_status(this)'>%s</div>"%(self.year,self.month,str(day),i,i))
            return self.day_cell(cssclass, '%s')%(''.join(body))
        return self.day_cell('noday', ' %s')%(''.join(body))

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        as_is = """<table border="0" cellpadding="0" cellspacing="0" class="month">"""
        to_be = """<table border="0" cellpadding="0" cellspacing="0" class="month table table-bordered">"""
        return super(WorkoutCalendar, self).formatmonth(int(year), int(month)).replace(as_is,to_be)

    def group_by_day(self, workouts):
        field = lambda workout: workout.date.day
        return dict(
            [(day, list(items)) for day, items in groupby(workouts, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)


    def formatweek(self,theweek):
        s=''.join(self.formatday(d,wd) for (d,wd) in theweek)
        c=''.join(self.customerformat(d,wd) for (d,wd) in theweek)
        return '<tr class="tr-head">%s</tr>'%c +  '<tr>%s</tr>'%s

    def customerformat(self,day,weekday):
        if day != 0:
            return '<td class="td-head">%s月%s日</td>'%(self.month,day)
        return  '<td></td>'

@course_blueprint.route('/arrange/<string:year>/<string:month>',methods=('GET','POST'))
def arrange(year=datetime.date.today().year,month=datetime.date.today().month):
    my_workouts = Single_course.query.filter(
                                    extract('year',Single_course.date) == year,
                                    extract('month',Single_course.date) == month).all()
    cal = WorkoutCalendar(my_workouts).formatmonth(year, month)
    #months=['01','02','03','04','05','06','07','08','09','10','11','12']
    #context ={'calendar': mark_safe(cal),'step':step,'months':months}
    return render_template('course/arrange.html',cal=cal)
