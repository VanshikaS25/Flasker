from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#initialize db
db = SQLAlchemy()
#Create flask instance
app = Flask(__name__)

# add mysql database
# create db first
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:asdfghjkl@localhost/flask_users'
app.config['SECRET_KEY'] = "password"
db.init_app(app)

#Create model
class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(200), nullable=False, unique=True)
	date_added = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<Name %r>' % self.name 

class UserForm(FlaskForm):
	name = StringField("Name", validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired()])
	submit = SubmitField("Submit")

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
	name = None
	form = UserForm()
	#validate form
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user is None:
			user = Users(name=form.name.data, email=form.email.data)
			db.session.add(user)
			db.session.commit()
		name = form.name.data
		form.name.data = ''
		form.email.data = ''
		flash("Form Submitted Successfully")

	our_users = Users.query.order_by(Users.date_added)
	return render_template("add_user.html", form=form, name=name, our_users=our_users)


# Update db
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
	form = UserForm()
	name_to_update = Users.query.get_or_404(id)
	if request.method == 'POST':
		name_to_update.name = request.form['name']
		name_to_update.email = request.form['email']
		try:
			db.session.commit()
			flash("User updated Successfully")
			return render_template("update.html", form=form,
				name_to_update=name_to_update)
		except:
			flash("OOPS.. Something's not right")
			return render_template("update.html", form=form,
				name_to_update=name_to_update)
	else:
		flash("OOPS.. Something's not right")
			return render_template("update.html", form=form,
				name_to_update=name_to_update)


# Create a form class
class NamerForm(FlaskForm):
	name = StringField("What is your name?", validators=[DataRequired()])
	submit = SubmitField("Submit")

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

# Create name page
@app.route('/name', methods=['GET', 'POST'])
def name():
	name = None
	form = NamerForm()
	#validate form
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = ''
		flash("Form Submitted Successfully")
	return render_template("name.html", name=name, 
		form = form)

if __name__ == "__main__":
	app.run(debug=True)