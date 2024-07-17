import psycopg2
from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:shubham@localhost:5432/flask_database'

db = SQLAlchemy(app)

class Students(db.Model):
    Roll_no = db.Column(db.Integer,primary_key = True,autoincrement=True)
    Name = db.Column(db.String(200),nullable=False)
    Marks = db.Column(db.Integer)

with app.app_context():
    db.create_all()

@app.route('/students')
def get_studentinfo():
    students = Students.query.all()
    students_info=[
        {'Roll_no':student.Roll_no,'Name':student.Name,'Marks':student.Marks} for student in students
    ]
    return jsonify({"students_info":students_info})

@app.route('/addinfo',methods=["POST"])
def create_task():
    data = request.get_json()
    new_student = Students(Name = data['name'],Marks=data['marks'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"massage":"Student info added succefully"}),201

@app.route('/rollno', methods=["POST"])
def getby_rollno():
    data = request.get_json()
    roll_no = data.get('rollno')  
    if roll_no:
        student = Students.query.get(roll_no)
        if student:
            return jsonify({'Roll_no': student.Roll_no, 'Name': student.Name, 'Marks': student.Marks})
    return jsonify({"error": "Enter valid roll number"}), 400

@app.route('/updateinfo',methods=["POST"])
def update_info():
    data = request.get_json()
    roll_no = data.get('rollno') 
    student = Students.query.get(roll_no) 
    if student:
        student.Name=data['name']
        student.Marks=data['marks']
        db.session.commit()
        return jsonify({"massage":"student info updated sucessfully"})
    else:
        return jsonify({"massage":"student not found"})
    
@app.route('/delete',methods=["POST"])
def delete_info():
    data = request.get_json()
    roll_no = data.get('rollno') 
    student = Students.query.get(roll_no)
    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify({"massage":"student info deleted sucessfully"})
    else:
        return jsonify({"massage":"student not found"})


if __name__ == ('__main__'):
    app.run(debug=True)