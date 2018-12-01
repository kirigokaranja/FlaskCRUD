import os

from flask import Flask , render_template
from flask import request
import json

from flask_sqlalchemy import SQLAlchemy
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "flaskcrud.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class User(db.Model):
    fname = db.Column(db.String(80), unique=True,nullable=False)
    sname = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return "<User: {}>".format(self.email)

class Business(db.Model):
    name = db.Column(db.String(80), unique=True,nullable=False, primary_key=True)
    owner = db.Column(db.String(80), unique=True, nullable=False)
    location = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return "<Business: {}>".format(self.name)


@app.route('/')
@app.route('/hello')
def hello():
    return 'Hello, Kirigo Karanja!'

@app.route('/home')
def home():
    title = "My Name"
    application = {
        'heading': 'new intro to andela'
    }
    return render_template("home.html", name=title, application = application)

@app.route('/login', methods=["get", "post"])
def login():
    if request.form:
        email = request.form['email']
        password = request.form['password']

        enm = User.query.filter_by(email=email).first()

        if email == enm:
            return render_template("home.html")


    return render_template("Login.html")

@app.route('/signin', methods=["get", "post"])
def signin():
    if request.form:
        print(request.form)
        fname = request.form['fname']
        sname = request.form['sname']
        email = request.form['email']
        password = request.form['password']

        user = User(fname=request.form['fname'], sname=request.form['sname'], email=request.form['email'], password=request.form['password'] )
        db.session.add(user)
        db.session.commit()

        userdict = {
            "firstname": fname,
            "lastname": sname,
            "email": email,
            "password": password
        }
        print(userdict)
        with open('result.json', 'w') as fp:
            json.dump(userdict, fp)

        users = User.query.all()
        return render_template("home.html", users=users)

    return render_template("SignIn.html")

@app.route('/businesses', methods=["get", "post"])
def registerbusiness():
    if request.form:
        print(request.form)

        business = Business(name=request.form['name'], owner=request.form['owner'], location=request.form['location'],
                    description=request.form['description'])
        db.session.add(business)
        db.session.commit()

        businesses = Business.query.all()
        return render_template('home.html', businesses=businesses)

    return render_template('business.html')

if __name__ == '__main__':
    app.run(debug=True)