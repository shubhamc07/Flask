import psycopg2
import re
from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:shubham@localhost:5432/flask_database'

db = SQLAlchemy(app)

class Employees(db.Model):
    Emp_id = db.Column(db.Integer,primary_key=True)
    Emp_name = db.Column(db.String(200),nullable=False)
    Emp_email = db.Column(db.String(200),unique=True,nullable=False)
    Emp_age = db.Column(db.Integer,CheckConstraint('age>=18 AND age <=60',name='check working age'))
    Emp_dept = db.Column(db.String(200))
    Emp_salary = db.Column(db.Integer,nullable=False)
    

with app.app_context():
    db.create_all()

@app.route('/empdata',methods=["GET"])
def empdata():
    employees = Employees.query.all()
    emp_list =[
        {'Emp_id':employee.Emp_id,'Emp_name':employee.Emp_name,'Emp_dept':employee.Emp_dept,'Emp_salary':employee.Emp_salary} for employee in employees
    ]
    return jsonify({"Employees_Data":emp_list})

@app.route('/add_empdata',methods=["POST"])
def add_empdata():
    data = request.get_json()
    new_employee = Employees(Emp_name=data['name'],Emp_email=data['email'],Emp_age=data['age'],Emp_dept=data['dept'],Emp_salary=data['salary'])
    email_check = r'^([A-Za-z0-9_\-\.])+@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$'

    if not(data['age']>=18 and data['age']<=60):
        return jsonify({"error":"employee age must between 18 to 60"})
    elif not re.match(email_check,data['email']):
        return jsonify({"error":"enter a  valid email"})
    else:
        db.session.add(new_employee)
        db.session.commit()
        return jsonify({'massage':"Employee Details Added Sucessfully"})

@app.route('/getby_empid',methods=["POST"])
def getby_empid():
    data = request.get_json()
    emp_id = data['empid']
    if emp_id:
        employee = Employees.query.get(emp_id)
        if employee:
            return jsonify({'Emp_id': employee.Emp_id, 'Emp_name': employee.Emp_name,'Emp_email':employee.Emp_email,'Emp_age':employee.Emp_age,'Emp_dept': employee.Emp_dept,'Emp_salary':employee.Emp_salary})
    else:
        return jsonify({"error":"No record found"})


@app.route('/update_empdata',methods=["POST"])
def update_empdata():
    data = request.get_json()
    emp_id = data['empid']
    employee = Employees.query.get(emp_id)
    if employee:
        employee.Emp_name=data['empname']
        employee.Emp_email=data['email']
        employee.Emp_age=data['age']
        employee.Emp_dept=data['dept']
        employee.Emp_salary=data['salary']
        db.session.commit()
        return jsonify({"massage":"Employee Data Updated Sucessfully"})
    else:
        return jsonify({"error":"Unable to get Employee Data"})

@app.route('/delete',methods=["POST"])
def delete_empdata():
    data = request.get_json()
    emp_id = data['empid']
    if emp_id:
        employee = Employees.query.get(emp_id)
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'Emp_id': employee.Emp_id, 'Emp_name': employee.Emp_name,'Emp_email':employee.Emp_email,'Emp_age':employee.Emp_age, 'Emp_dept': employee.Emp_dept,'Emp_salary':employee.Emp_salary},{"massage":"Employee Data Deleted Successfully"})
    else:
        return jsonify({"error":"Enter a valid Employee Id"})


