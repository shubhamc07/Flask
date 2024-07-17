import re
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:shubham@localhost:5432/flask_database'

db = SQLAlchemy(app)

class Players(db.Model):
    Player_id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer, CheckConstraint('age >= 16', name='check_players_age'))
    Number = db.Column(db.String(100), unique=True, nullable=False)
    Address = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()


def validate_player_data(data):
    errors = []
    name = data.get('name')
    email = data.get('email')
    age = data.get('age')
    number = data.get('number')
    address = data.get('address')

    if not name or not re.match(r'^[A-Za-z]+(?: [A-Za-z]+)*$', name):
        errors.append('Enter a valid name')
    if not email or not re.match(r'^([A-Za-z0-9_\-\.])+@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$', email):
        errors.append("Enter a valid email")
    if not number or not re.match(r'^[0-9]{10}$', number):
        errors.append("Enter a valid number")
    if not age or int(age) < 16:
        errors.append("You cannot play in the senior team until you are 16")
    if not address:
        errors.append("Enter your Address")

    return errors


@app.route('/add_player', methods=["POST"])
def add_player():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Enter data"})

    errors = validate_player_data(data)
    if errors:
        return jsonify({"errors": errors})

    name = data.get('name')
    email = data.get('email')
    age = data.get('age')
    number = data.get('number')
    address = data.get('address')
    new_player = Players(Name=name, Email=email, age=age, Number=number, Address=address)

    try:
        db.session.add(new_player)
        db.session.commit()
        return jsonify({'message': "Player Details Added Successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to add player details", "details": str(e)})
    
@app.route('/showdata')
def showdata():
    players = Players.query.all()
    players_list = [{'Player_id': player.Player_id, 'Name': player.Name, 'Email': player.Email, 'Age': player.age,
                     'Number': player.Number, 'Address': player.Address} for player in players]
    return jsonify({"Players Data": players_list})


@app.route('/update_player/<int:player_id>', methods=['PATCH'])
def update_player(player_id):
    data = request.get_json()
    player = Players.query.get(player_id)

    if not player:
        return jsonify({"error": f"Player with ID {player_id} not found"})

    try:
        for key, value in data.items():
            if hasattr(player, key):
                setattr(player, key, value)
            else:
                return jsonify({"error": f"Attribute '{key}' not present in table"})
        db.session.commit()
        return jsonify({"message": f"Player details of {player_id} have been updated"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)})
    
@app.route('/delete_player/<int:player_id>', methods=['DELETE'])
def delete_player(player_id):
    player = Players.query.get(player_id)

    if player:
        db.session.delete(player)
        db.session.commit()
        return jsonify({"massage":"Players Data Deleted Successfully"})
    else:
        return jsonify({"error":"Player not found"})


if __name__ == '__main__':
    app.run(debug=True)