from flask import Flask,request,render_template,jsonify,redirect,url_for,flash
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,EqualTo


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

class Regform(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    

@app.route('/register',methods=['GET','POST'])
def register():
    form = Regform()
    if form.validate_on_submit():
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/')
def home():
    return 'Home Page'

if __name__ == '__main__':
    app.run(debug=True)