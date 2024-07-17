import re
from flask import Flask,request,jsonify

app = Flask(__name__)

@app.route('/fdata',methods=["POST"])
def fdata():
    data = request.get_json()
    fname = data['fname']
    lname = data['lname']
    email= data['email']
    phone = data['phone']
    gender = data['gender']

    name_check = r'^[A-Za-z]+(?: [A-Za-z]+)*$'
    email_check = r'^([A-Za-z0-9_\-\.])+@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$'
    num_check = r'^[0-9]{10}$'

    if not data:
        return jsonify({"Error":"enter data"}),400
    
    errors={}
    if not re.match(name_check,fname):
        errors.update({"nameError":'Enter valid first name'})
    if not re.match(name_check,lname):
        errors.update({"nameerror":'Enter valid last name'})
    if not re.match(email_check,email):
        errors.update({"emailError":'Enter valid email address'})
    if not re.match(num_check,phone):
        errors.update({"numberrror":'Enter valid phone number'})
    
    if errors:
        return jsonify({"errors": errors}), 400
    else:
        return jsonify({"message": "valid data"},data), 200
    

if __name__ == ('__main__'):
    app.run(debug=True)
