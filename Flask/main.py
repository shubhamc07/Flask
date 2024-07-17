from flask import Flask,request

app = Flask(__name__)

@app.route("/")
def hello_shubham():
    return "<h1>Hello, shubham</h1>"

@app.route("/xyz")
def xyz():
    return "<h1>Hello, xyz</h1>"

@app.route('/greet/<name>')
def greet(name):
    return f"<h1>Hello {name}</h1>"

@app.route('/add/<int:number1>/<int:number2>')
def add(number1,number2):
    return f"{number1} + {number2} = {number1 + number2}"

# url parameters
@app.route('/handle_url_params')
def handle_params():
    if 'greeting' in request.args.keys() and 'name' in request.args.keys():
        greeting = request.args['greeting']
        name = request.args.get('name')
        return f"{greeting}, {name}"
    else:
        return "Some parameters are missing"

app.run(debug=True)