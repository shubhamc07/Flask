from flask import Flask,request,jsonify

app = Flask(__name__)

dict ={
    "id":1,
    "name":"shubham"
}

@app.route('/update',methods=['POST'])
def update():
    data = request.get_json()
    dict.update(data)
    return jsonify(dict)

list = ["shubham","raj","vansh"]
@app.route('/list_data',methods=['GET'])
def list_data():
    return jsonify(list)


if __name__ == ('__main__'):
    app.run(debug=True)