import psycopg2
from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:shubham@localhost:5432/flask_database'

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    title = db.Column(db.String(200),nullable=False)
    done = db.Column(db.Boolean,default=False)

with app.app_context():
    db.create_all()

@app.route('/tasks')
def get_tasks():
    tasks = Task.query.all()
    task_list=[
        {'id':task.id,'title':task.title,'done':task.done} for task in tasks
    ]
    return jsonify({"tasks":task_list})

@app.route('/addtasks',methods=["POST"])
def create_task():
    data = request.get_json()
    new_task = Task(title = data['title'],done=data['done'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"massage":"Task created succefully"}),201




if __name__ == ('__main__'):
    app.run(debug=True)