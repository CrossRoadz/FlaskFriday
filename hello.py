from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#flask instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "qqqQQQqqq"

#create a form class
class NamerForm(FlaskForm):
	name = StringField("Input your name here", validators=[DataRequired()])
	submit = SubmitField("Submit")



#create route decorator
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/user/<name>")
def user(name):
	return render_template("user.html",name=name)


@app.route("/name", methods=['GET', 'POST'])
def name():


	name = None
	form = NamerForm()

	#validate form
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = ""
		flash("Name Submitted Successfully!")

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

