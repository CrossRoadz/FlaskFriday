from flask import Flask, render_template

#flask instance
app = Flask(__name__)

#create route decorator
@app.route("/")
def index():
	stuff = "this is bold text"
	pizza = ["Pepperoni", "Cheese","Mushroom",41]
	return render_template("index.html",
		stuff = stuff,
		pizza=pizza)

@app.route("/user/<name>")
def user(name):
	return render_template("user.html",name=name)

#custom error pages

# invalid url
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

# interal server error
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500