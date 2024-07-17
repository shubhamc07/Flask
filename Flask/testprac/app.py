from flask import Flask,render_template,request,jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:shubham@localhost:5432/flask_database"

db = SQLAlchemy(app)


class Test(db.Model):
    id = db.Cloumn(db.Integer,primary_key=True,autoincrement=True)
    name = db.Cloumn(db.String(100),nullable=False)
    done = db.Column(db.Boolean,default=False)

with app.app_context():
    db.create_all()


@app.route("/add_test",methods=['POST'])
def addtest():
    data = request.get_json()
    test_name = data['testname']
    done = data['done']
    new_test = Test(name=test_name,done=done)
    db.session.add()
    db.session.commit()
    return jsonify({'msg:test added'})

@app.route('/showtest',methods=['GET'])
def showtest():
    tests = Test.query.all()
    test_list = [{'id':test.id,"name":test.name,'done':test.done} for test in tests]
    return jsonify({'tests':test_list})

@app.route('/getbyid',methods=['POST'])
def getbyid():
    data = request.get_json()
    id = data['id']
    if id:
        test = Test.query.get(id)
        if test:
            return jsonify({'id':test.id,'name':test.name,'done':test.done})
    return jsonify({'error':"enter valid id"})
    





@app.route('/',methods=['POST'])
def home():
    return render_template()
    
@app.route('/cal',methods=['POST'])
def cal():
    num1 = float(request.form["num1"])
    num2 = float(request.form["num2"])
    ops = request.form["opration"]
    if ops == 'add':
        result = num1 + num2
    elif ops == 'sub':
        result = num1 - num2
    elif ops == 'mul':
        result = num1 * num2
    elif ops == 'div':
        if num2 != 0:
            result = num1 / num2
        else:
            result = 'Zero Division Error'
    return render_template(index.html,result=result,num1=num1,num2=num2)


@app.route('add/<int:num1>/<int:num2>',methods=['GET'])
def add(num1,num2):
    res = num1 + num2
    return jsonify(res)




