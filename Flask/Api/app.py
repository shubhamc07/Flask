from flask import Flask,jsonify,request

app = Flask(__name__)

@app.route('/add/<int:num1>/<int:num2>',methods=['GET'])
def add(num1,num2):
    res = num1 + num2
    return jsonify(res,200)

@app.route('/addtion',methods=['POST'])
def addtion():
    data = request.get_json()
    num1 = data['num1']
    num2 = data['num2']
    res = num1 + num2
    return jsonify({"addtion is":+res})



if __name__ == ('__main__'):
    app.run(debug=True)
