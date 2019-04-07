
from flask import abort
from flask_restful import Api,Resource,fields,marshal_with
from .models import *

course_api = Api()

people_fields ={
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

category_fields ={'name':fields.String()}
class Category_api(Resource):
    @marshal_with(category_fields)
    def get(self):
        return Category.query.all()
course_api.add_resource(Category_api,'/api/category',endpoint='category_api')

course_api.add_resource(Course_api,
                        '/api/course',
                        '/api/course/<int:id>',
                        endpoint='api')

course_api.add_resource(People_api,
                        '/api/<string:role>',
                        '/api/<string:role>/<int:id>',
                        endpoint='people_api')
