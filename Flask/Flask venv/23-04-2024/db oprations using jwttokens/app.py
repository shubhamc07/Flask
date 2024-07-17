import jwt
import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:shubham@localhost:5432/flask_database'
app.config['SECRET_KEY']='ctUPvuvMkGOG_w'

db = SQLAlchemy(app)

class Admin(db.Model):
    admin_id = db.Column(db.Integer,primary_key=True)
    admin_name = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200),nullable=False)
    name = db.Column(db.String(200), unique=True, nullable=False)
 
with app.app_context():
    db.create_all()

def token_required(f):
    @wraps(f)
    def deco_function(*args, **kwargs):
        Auth = request.headers.get('Auth')
        if not Auth:
            return jsonify({'message': 'Token is missing'})

        try:
            decoded_token = jwt.decode(Auth, app.config['SECRET_KEY'], algorithms=['HS256'])
            admin_id = decoded_token.get('admin_id')
            admin = Admin.query.filter_by(admin_id=admin_id).first()

            if not admin:
                return jsonify({"error": "Admin details not found"})

            return f(admin, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'})
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'})

    return deco_function

@app.route('/add_admin',methods=["POST"])
def add_admin():
    data = request.get_json()
    admin_name = data['aname']
    password = data['password']
    name = data['name']

    new_admin = Admin(admin_name=admin_name,password=password,name=name)

    try:
        db.session.add(new_admin)
        db.session.commit()
        return jsonify({'message': "Admin Details Added Successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to add admin details", "details": str(e)})
    
@app.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    admin_name = data['aname']
    password = data['password']

    admin = Admin.query.filter_by(admin_name=admin_name, password=password).first()

    if admin:
        token = jwt.encode({'admin_id':admin.admin_id, "exp":datetime.datetime.utcnow() + datetime.timedelta(seconds=120)},app.config['SECRET_KEY'],algorithm='HS256')
        return jsonify({'token': token})
    else:
        return jsonify({'message': 'Invalid username or password'})
    

@app.route('/getbytoken', methods=['POST'])
@token_required
def getbytoken(admin):
    return jsonify({'admin_id': admin.admin_id, 'admin_name': admin.admin_name, 'name': admin.name})


if __name__ == '__main__':
    app.run(debug=True)
