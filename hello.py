from flask import Flask, render_template

#Create flask instance
app = Flask(__name__)

@app.route('/')

def index():
	fav_pizza = ["Cheese", "Pepperoni", "Mozzeralla", 41]
	return render_template("index.html", 
		name = "Vanshika",
		fav_pizza = fav_pizza)

#localhost:5000/user/vanshika
@app.route('/user/<name>')
def user(name):
	return render_template("user.html", name=name)

#Custom Error pages
@app.errorhandler(404)
def pafe_not_found(e):
	return render_template("404.html"), 404

@app.errorhandler(500)
def pafe_not_found(e):
	return render_template("500.html"), 500

if __name__ == "__main__":
	app.run(debug=True)