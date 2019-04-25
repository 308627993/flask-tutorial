
from flask import abort
from flask_restful import Api,Resource,fields,marshal_with,reqparse,request
from .models import *
from .views import WorkoutCalendar
from sqlalchemy import extract
import json
from datetime import datetime,timedelta

course_api = Api()

people_fields ={
    'id':fields.Integer(),
    'name':fields.String(),
    'gender':fields.String(),
    'birthday':fields.DateTime(dt_format='iso8601')
}
class Course_api(Resource):
    def get(self,id=None):
        if id:
            return {'id':id}
        return {'hello':'word'}

class People_api(Resource):
    @marshal_with(people_fields)
    def get(self,role,id=None):
        if id:
            if role =='student':
                person = Student.query.get(id)
            elif role == 'teacher':
                person = Teacher.query.get(id)
            if not person:
                abort(404)
            return person
        else:
            if role == 'student':
                people = Student.query.all()
            elif role == 'teacher':
                people = Teacher.query.all()
            return people

class Category_People_api(Resource):
    @marshal_with(people_fields)
    def get(self,category_id = None):
        if category_id :
            category = Category.query.get(category_id)
            return [category.teachers.all(),category.students.all()]
        else:
            return None
course_api.add_resource(Category_People_api,'/api/people/<string:category_id>',endpoint='teachers_api')


category_fields ={'name':fields.String(),'id':fields.Integer()}
class Category_api(Resource):
    @marshal_with(category_fields)
    def get(self):
        return Category.query.all()
course_api.add_resource(Category_api,'/api/category',endpoint='category_api')

workout_post_parser = reqparse.RequestParser()
workout_post_parser.add_argument(
    'course_infos',
    type=str,
    required = True,
    help = "select items are required"
    )
workout_post_parser.add_argument(
    'teacher_id',
    type=str,
    required = True,
    help = "teacher's id is required"
    )
workout_post_parser.add_argument(
    'student_id',
    type=str,
    required = True,
    help = "student's id is required"
    )

class Workout_api(Resource):
    def get(self,year,month,teacher_id=None,student_id=None):
        objs = Single_course.query.filter(
                                        extract('year',Single_course.date) == year,
                                        extract('month',Single_course.date) == month)
        if teacher_id == student_id == None:
            my_workouts = []#objs.all()
        elif (teacher_id == None and student_id != None):
            my_workouts = objs.filter_by(student_id = student_id).all()
        elif (teacher_id != None and student_id == None):
            my_workouts = objs.filter_by(teacher_id = teacher_id).all()
        elif (teacher_id != None and student_id != None):
            my_workouts = objs.filter_by(teacher_id = teacher_id,student_id = student_id).all()
        cal = WorkoutCalendar(my_workouts).formatmonth(year, month)
        return {'data':cal}
    def post(self,year,month,teacher_id,student_id):
        args = workout_post_parser.parse_args(strict=True)
        return args
course_api.add_resource(Workout_api,
                        '/api/workout/<int:year>/<int:month>',
                        '/api/workout/<int:year>/<int:month>/student/<int:student_id>',
                        '/api/workout/<int:year>/<int:month>/teacher/<int:teacher_id>',
                        '/api/workout/<int:year>/<int:month>/<int:teacher_id>/<int:student_id>',
                        endpoint='workout_api')


course_api.add_resource(Course_api,
                        '/api/course',
                        '/api/course/<int:id>',
                        endpoint='api')

course_api.add_resource(People_api,
                        '/api/<string:role>',
                        '/api/<string:role>/<int:id>',
                        endpoint='people_api')

def create_single_course(student_id,teacher_id,section,date):
    new_course = Single_course(date,section)
    new_course.student_id = student_id
    new_course.teacher_id = teacher_id
    return new_course

def save_objs(obj_list):
    for obj in obj_list:
        db.session.add(obj)
    db.session.commit()
def delete_objs(obj_list):
    for obj in obj_list:
        db.session.delete(obj)
    db.session.commit()

class Arrange_api(Resource):
    def post(self):
        data = (request.get_data()).decode()
        data_dic = {i.split('=')[0]:i.split('=')[1] for i in data.split('&')}
        date_list = []
        create_objs = []
        exist_objs = []
        error_teacher_objs = []
        error_student_objs = []
        startday,endday,weekday = datetime.strptime(data_dic['startday'], "%Y-%m-%d"),datetime.strptime(data_dic['endday'], "%Y-%m-%d"),int(data_dic['weekday'])
        student_id,teacher_id,section = int(data_dic['student']),int(data_dic['teacher']),data_dic['section']
        while startday <= endday:
            if startday.weekday() + 1 == weekday:
                date_list.append(startday.date())
            startday += timedelta(days=1)
        for day in date_list:
            match_student_course = Single_course.query.filter_by(student_id = student_id,section=section,date=day).first()
            match_teacher_course = Single_course.query.filter_by(teacher_id=teacher_id,section=section,date=day).first()
            if match_student_course == match_teacher_course:
                if match_student_course:
                    exist_objs.append(match_student_course)
                else:
                    create_objs.append(create_single_course(student_id,teacher_id,section,day))
            else:
                if match_student_course:
                    error_student_objs.append(match_student_course)
                if match_teacher_course:
                    error_teacher_objs.append(match_teacher_course)
        save_objs(create_objs)
        exist_data =[{'teacher':i.teacher.name,'student':i.student.name,'date':str(i.date),'section':i.section,'id':i.id } for i in exist_objs]
        create_data =[{'teacher':i.teacher.name,'student':i.student.name,'date':str(i.date),'section':i.section,'id':i.id } for i in create_objs]
        error_student_data = [{'teacher':i.teacher.name,'student':i.student.name,'date':str(i.date),'section':i.section,'id':i.id } for i in error_student_objs]
        error_teacher_data = [{'teacher':i.teacher.name,'student':i.student.name,'date':str(i.date),'section':i.section,'id':i.id } for i in error_teacher_objs]
        print('section:',section)
        return json.dumps({'exist_data':exist_data,'create_data':create_data,'error_teacher_data':error_teacher_data,'error_student_data':error_student_data})

course_api.add_resource(Arrange_api,'/api/course_arrange',endpoint='course_arrange_api')

class Course_delete_api(Resource):
    def post(self):
        data = (request.get_data()).decode(encoding='UTF-8',errors='strict')
        ids =json.loads(data)['ids']
        objs = [Single_course.query.get(i) for i in ids]
        delete_objs(objs)
        return json.dumps(data)
course_api.add_resource(Course_delete_api,'/api/course_delete')

class Item_create_api(Resource):
    def post(self,item):
        from urllib.parse import unquote
        data = (request.get_data()).decode(encoding='UTF-8',errors='strict')
        data_dic = {}
        for i in data.split('&'):
            a,b = i.split('=')
            data_dic[a] = unquote(b)  if a not in data_dic else data_dic[a]+ ('-*-' + unquote(b))
        print('data:**************',data)
        if item == 'category':
            name = data_dic['name'] if 'name' in data_dic else None
            if Category.query.filter_by(name=name).first():#查询该类名已经存在
                return json.dumps({'info':'already exist','result':'fail'})
            else:#该类名不存在，创建新的类
                try:
                    new_category = Category(name)
                    db.session.add(new_category)
                    db.session.commit()
                    info = '<%s> 创建成功！'%name
                    result = (new_category.id,name)
                except Exception as e:
                    info = '<%s> 创建失败，原因： [%s]'%(name,e)
                    result = 'fail'
                return json.dumps({'info':info,'result':result})
        elif item == 'student' or item == 'teacher':
            name = data_dic['name'] if 'name' in data_dic else None
            birthday = data_dic['birthday'] if 'birthday' in data_dic else None
            gender = data_dic['gender'] if 'gender' in data_dic else None
            categorys = (data_dic['categorys']).split('-*-') if 'categorys' in data_dic else None
            if (name and birthday and gender and categorys):
                if item == 'student':
                    new_people = Student(name,gender,datetime.strptime(birthday, "%Y-%m-%d"))
                elif item == 'teacher':
                    new_people = Teacher(name,gender,datetime.strptime(birthday, "%Y-%m-%d"))
                [new_people.categorys.append(Category.query.get(category)) for category in categorys]
                db.session.add(new_people)
                db.session.commit()
course_api.add_resource(Item_create_api,'/api/item_create/<string:item>',endpoint='item_create_api')
