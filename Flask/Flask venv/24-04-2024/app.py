#Shubham Chavan

import jwt
import re
import datetime
from functools import wraps
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:shubham@localhost:5432/flask_database'
app.config['SECRET_KEY']='fxi031RaCekGncj1'

db = SQLAlchemy(app)

class College(db.Model):
    __tablename__ = 'college'
    college_id = db.Column(db.Integer,primary_key=True)
    college_name = db.Column(db.String(200),unique=True,nullable=False)
    password = db.Column(db.String(200),nullable=False)
    location = db.Column(db.String(120))
    students = db.relationship('Students',backref='college')


class Students(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer,primary_key=True)
    student_name = db.Column(db.String(200),nullable=False)
    course = db.Column(db.String(200),nullable=False)
    student_class = db.Column(db.String(200),nullable=False)
    student_phone_no = db.Column(db.String(200),unique=True,nullable=False)
    college_id = db.Column(db.Integer,db.ForeignKey('college.college_id'),nullable=False)


with app.app_context():
    db.create_all()


def token_required(f):
    @wraps(f)
    def deco_func(*args,**kwargs):
        Auth = request.headers.get('Auth')
        if not Auth:
            return jsonify({'message':'token is missing'})
        
        try:
            decoded_token = jwt.decode(Auth,app.config['SECRET_KEY'],algorithms=['HS256'])
            college_id = decoded_token.get('college_id')
            college = College.query.filter_by(college_id=college_id).first()

            if not college:
                return jsonify({"error": "admin details not found"})

            return f(college, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'token has expired'})
        except jwt.InvalidTokenError:
            return jsonify({'message': 'invalid token'})

    return deco_func



def validate_college_data(data):
    errors = []
    college_name = data.get('cname')
    password = data.get('password')
    location = data.get('location')

    if not college_name or not re.match(r'^[A-Za-z]+(?: [A-Za-z]+)*$', college_name):
        errors.append('Enter a valid college name')

    if not password or len(password) < 6:
        errors.append("Password must be at least 6 characters long")

    if not location:
        errors.append("Enter the college's location")

    return errors



def validate_student_data(data):
    errors = []
    student_name = data.get('sname')
    course = data.get('course')
    student_class = data.get('class')
    student_phone_no = data.get('number')

    if not student_name or not re.match(r'^[A-Za-z]+(?: [A-Za-z]+)*$', student_name):
        errors.append('Enter a valid student name')

    if not course:
        errors.append("Enter the student's course")

    if not student_class:
        errors.append("Enter the student's class")

    if not student_phone_no or not re.match(r'^[0-9]{10}$', student_phone_no):
        errors.append("Enter a valid 10-digit phone number")

    return errors



@app.route('/add_clg',methods=['POST'])
def add_clg():
    data = request.get_json()

    validation_errors = validate_college_data(data)
    
    if validation_errors:
        return jsonify({"error": "Validation error", "details": validation_errors})

    college_name = data['cname']
    password = data['password']
    location = data['location']

    new_college = College(college_name=college_name,password=password,location=location)

    try:
        db.session.add(new_college)
        db.session.commit()
        return jsonify({"massage":"college details added sucessfullly"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "failed to add College details", "details": str(e)})



@app.route('/clg_login',methods=["POST"])
def clg_login():
    data = request.get_json()
    college_name = data['cname']
    password = data['password']

    college = College.query.filter_by(college_name=college_name,password=password).first()

    if college:
        token = jwt.encode({'college_id':college.college_id,"exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=15)},app.config['SECRET_KEY'],algorithm='HS256')
        return jsonify({"token":token})
    else:
        return jsonify({'message': 'invalid college_name or password'})



@app.route('/getclg_bytoken',methods=['GET'])
@token_required
def getclg_bytoken(college):
    return jsonify({'college_id':college.college_id,'college_name':college.college_name,"password":college.password,"location":college.location})



@app.route('/add_student',methods=["POST"])
@token_required
def add_student(college):
    data = request.get_json()

    validation_errors = validate_student_data(data)
    
    if validation_errors:
        return jsonify({"error": "Validation error", "details": validation_errors})

    student_name = data['sname']
    course = data['course']
    student_class = data['class']
    student_phone_no = data['number']
    college_id = college.college_id

    if not college_id:
        return jsonify({"massage":"college not found"})

    student = Students(college_id=college_id,student_name=student_name,course=course,student_class=student_class,student_phone_no=student_phone_no)

    try:
        db.session.add(student)
        db.session.commit()
        return jsonify({"massage":"student details added sucessfullly"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "failed to add student details", "details": str(e)})



@app.route('/get_student/<int:student_id>', methods=['GET'])
@token_required
def get_student(college, student_id):
    college_id = college.college_id

    student = Students.query.filter_by(student_id=student_id, college_id=college_id).first()

    if not student:
        return jsonify({"error": f"student with id {student_id} not found in this college"})

    student_info = {
        'student_id': student.student_id,
        'student_name': student.student_name,
        'course': student.course,
        'student_class': student.student_class,
        'student_phone_no': student.student_phone_no
    }

    return jsonify({"student": student_info})



@app.route('/get_all_students',methods=['GET'])
@token_required
def get_all_students(college):
    college_id = college.college_id
    if college_id:
            students = Students.query.filter_by(college_id=college_id).all()
            students_list=[
                {'student_id':student.student_id,'student_name':student.student_name,'course':student.course,'student_class':student.student_class,'student_phone_no':student.student_phone_no} for student in students
            ]

            college_info = {
                'college_id':college.college_id,
                'college_name':college.college_name,
                "password":college.password,
                "location":college.location,
                'students': students_list
            }
            return jsonify({"college":college_info })
    else:
        return jsonify({"error": "college not found."})



@app.route('/update_students/<int:student_id>',methods=['PATCH'])
@token_required
def update_students(college, student_id):
    data = request.get_json()
    college_id = college.college_id

    student = Students.query.filter_by(student_id=student_id, college_id=college_id).first()

    if not student:
        return jsonify({"error": f"student with id {student_id} not found for this college"})

    try:
        for key, value in data.items():
            if hasattr(student, key):
                setattr(student, key, value)
            else:
                return jsonify({"error": f"attribute '{key}' not present in student table"})
        db.session.commit()
        return jsonify({"message": f"student details of id {student_id} have been updated"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)})



@app.route('/delete_student/<int:student_id>', methods=['DELETE'])
@token_required
def delete_student(college, student_id):
    college_id = college.college_id

    student = Students.query.filter_by(student_id=student_id, college_id=college_id).first()

    if not student:
        return jsonify({"error": f"student with id {student_id} not found in this college"})

    try:
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": f"student with id {student_id} has been deleted"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)})



if __name__ == ('__main__'):
    app.run(debug=True)