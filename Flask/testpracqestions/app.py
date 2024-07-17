from flask import Flask,render_template,request,jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/q1')
def home():
    return "Hello,World"

@app.route('/greet',methods=["POST"])
def greet():
    name = request.form['name']
    return f'Hello,{name}!'

@app.route('/q3/<name>')
def q3(name):
    return f"Welcome,{name}!"

@app.route('/q4')
def q4():
    msg = "Hello this msg is comeing from flask"
    return render_template('msg.html',msg=msg)




if __name__ == '__main__':
    app.run(debug=True)