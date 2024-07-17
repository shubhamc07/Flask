from flask import Flask,request,jsonify

app = Flask(__name__)

@app.route('/oddeven/<int:num>',methods=["GET"])
def oddeven(num):
    if num % 2==0:
        return jsonify({'Number is Even'})
    else:
        return jsonify({'Number is Odd'})
    
@app.route('/evenodd',methods=["POST"])
def evenodd():
    data = request.get_json()
    num = data['num']
    if num % 2 == 0:
        return jsonify({"Number is even"})
    else:
        return jsonify({"Number is odd"})
    
if __name__ == ('__main__'):
    app.run(debug=True)


