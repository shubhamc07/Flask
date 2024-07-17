import re
from flask import Flask,request,jsonify

app = Flask(__name__)

@app.route('/formdata',methods=["POST"])
def formdata():
    data = request.get_json()
    frist_name = data['fname']
    last_name = data['lname']
    email= data['email']
    phone = data['phone']
    gender = data['gender']

    name_check = r'^[A-Za-z]+(?: [A-Za-z]+)*$'
    email_check = r'^([A-Za-z0-9_\-\.])+@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$'
    num_check = r'^[0-9]{10}$'
    if not data:
        return jsonify({"Error":"Enter data"}),400

    errors=[]
    if not re.match(name_check,frist_name):
        errors.append('Enter valid frist name')
    if not re.match(name_check,last_name):
        errors.append('Enter a valid last name')
    if not re.match(email_check,email):
        errors.append("Enter a valid email")
    if not re.match(num_check,phone):
        errors.append("Enter a valid number")
    if gender not in['male','female']:
        errors.append("Enter your gender")

    if errors:
        return jsonify({"errors": errors}), 400
    else:
        return jsonify({"message": "Data is valid"},data), 200
    
@app.route('/image',methods=["GET", "POST"])
def image():
    file = request.files['file']
    filename = file.filename
    if file:
        if filename.endswith('.jpeg') or filename.endswith('.jpg') or filename.endswith('.png'):
            return jsonify("File is valid",filename),200
        else:
            return jsonify("Enter valid file type"),400
    else:
        return jsonify("Select image"),400


        

if __name__ == ('__main__'):
    app.run(debug=True)