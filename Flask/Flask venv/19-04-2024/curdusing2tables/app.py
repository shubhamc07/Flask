import re
from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:shubham@localhost:5432/flask_database'

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer,primary_key=True)
    name =db.Column(db.String(200),unique=True,nullable=False)
    phone =db.Column(db.String(100),unique=True,nullable=False)
    email =db.Column(db.String(100),unique=True,nullable=False)
    address =db.Column(db.String(200),nullable=False)
    orders = db.relationship('Order',backref='users')


class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.user_id'),nullable=False)
    product_name = db.Column(db.String(100),nullable=False)

with app.app_context():
    db.create_all()


def validate_data(data):
    errors = []
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')
    address = data.get('address')
    product_name = data.get('pname')

    if not name or not re.match(r'^[A-Za-z]+(?: [A-Za-z]+)*$', name):
        errors.append('Enter a valid name')
    if not email or not re.match(r'^([A-Za-z0-9_\-\.])+@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$', email):
        errors.append("Enter a valid email")
    if not phone or not re.match(r'^[0-9]{10}$', phone):
        errors.append("Enter a valid number")
    if not address:
        errors.append("Enter your Address")
    if not product_name or not re.match(r'^[A-Za-z]+(?: [A-Za-z]+)*$',product_name):
        errors.append("Enter a valid product name")

    return errors

@app.route('/userdata',methods=["POST"])
def userdata():
    data= request.get_json()
    if not data:
        return jsonify({"error": "Enter data"})

    errors = validate_data(data)
    if errors:
        return jsonify({"errors": errors})
    
    user = User(name=data['name'], phone=data['phone'], email=data['email'],address =data['address'])
    order = Order(user_id=user.user_id,product_name=data['pname'])
    try:
        db.session.add(user)
        db.session.commit()
        db.session.add(order)
        db.session.commit()
        return jsonify({"massage":"user details and order added sucessfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to add user details and order", "details": str(e)})

@app.route('/showdata')
def joindata():
    data= db.session.query(User,Order).join(Order.users).all()
    data_list=[
        {'user_id':user.user_id,'name':user.name,'phone':user.phone,'email':user.email,'address':user.address,'order_id':order.order_id,'product_name':order.product_name} for user,order in data
    ]
    return jsonify({"data":data_list})

@app.route('/getbyid',methods=["POST"])
def getbyid():
    data = request.get_json()
    user_id = data['id']
    if user_id:
        user = User.query.get(user_id)

        if user:
            orders = Order.query.filter_by(user_id=user_id).all()
            order_list=[
                {'order_id':order.order_id,'product_name':order.product_name} for order in orders
            ]

            user_info = {
                'user_id': user.user_id,
                'name': user.name,
                'phone': user.phone,
                'email': user.email,
                'address': user.address,
                'orders': order_list
            }
            return jsonify({"User": user_info})
        else:
            return jsonify({"error": "User not found."}), 404
    else:
        return jsonify({"error": "User ID is required."})


@app.route('/add_order',methods=["POST"])
def add_order():
    data = request.get_json()
    user_id=data['id']
    product_name=data['pname']

    if not user_id or not product_name:
        return jsonify({"error": "User ID and product name are required."})
    
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found."}), 404

    order = Order(user_id=user_id, product_name=product_name)
    db.session.add(order)
    db.session.commit()

    return jsonify({"message": "Order placed successfully."})


@app.route('/update_data/<int:user_id>', methods=['PATCH'])
def update_data(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
        

    if not user:
        return jsonify({"error": f"User with ID {user_id} not found"})

    try:
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                return jsonify({"error": f"Attribute '{key}' not present in User table"})
        db.session.commit()
        return jsonify({"message": f"User details of {user_id} have been updated"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)})



@app.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if user:
        orders = Order.query.filter_by(user_id=user_id).all()
        for order in orders:
            db.session.delete(order)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"User and orders of {user_id} are deleted successfully."})
    else:
        return jsonify({"error": "User not found."})

if __name__ == ('__main__'):
    app.run(debug=True)



