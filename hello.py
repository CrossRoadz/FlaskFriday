from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#flask instance
app = Flask(__name__)
#add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#secert key
app.config['SECRET_KEY'] = "qqqQQQqqq"
#init database
app.app_context().push() #solves context error
db = SQLAlchemy(app)

#create model
class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(120), nullable=False, unique=True)
	date_added = db.Column(db.DateTime, default=datetime.utcnow)

	#create repr
	def __repr__(self):
		return "<Name %r>" % self.name

#create a form class
class UserForm(FlaskForm):
	name = StringField("Name", validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired()])
	submit = SubmitField("Submit")

class NamerForm(FlaskForm):
	name = StringField("Input name here", validators=[DataRequired()])
	submit = SubmitField("Submit")



#create route decorator
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/user/<name>")
def user(name):
	
	return render_template("user.html",name=name)

@app.route("/user/add", methods=["GET", "POST"])
def add_user():
	valid = False
	form = UserForm()

	#validate form
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user is None:
			valid = True
			user = Users(
				name=form.name.data,
				email=form.email.data
				)
			db.session.add(user)
			db.session.commit()
			flash("User Added Successfully!")
		else:
			flash("Failed to Add User, email is already taken")
		name = form.name.data
		form.name.data = ""
		form.email.data = ""
		
	our_users = Users.query.order_by(Users.date_added)

	return render_template("add_user.html",
		form=form,
		valid=valid,
		our_users=our_users)


@app.route("/name", methods=['GET', 'POST'])
def name():


	name = None
	form = NamerForm()

	#validate form
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = ""
		flash("Form Submitted Successfully!")

	return render_template('name.html',
		name=name,
		form=form)

#custom error pages

# invalid url
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

# interal server error
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500

#create a form class

