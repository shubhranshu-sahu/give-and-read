from flask import Flask , render_template , session , request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

import json

with open('config.json', 'r') as c:
    config = json.load(c)
    params = config["params"]
    social = config["social"]





# print(params['uri'])

app = Flask(__name__)

# Connecting to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/give_read'
db = SQLAlchemy(app)

@app.context_processor
def inject_globals():
    return {
        'social_links': social,
        'params': params
    }

class contact_us(db.Model):


    s_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    #__tablename__ = 'contact_us'  # Required if class name differs from table name
    # __tablename__ = 'books'   // not necessary , if not given , uses name of the class as table name !

    # def __init__(self, name, email, message):
        # self.name = name.Title()
        # self.email = email
        # self.message = message

    # // No need to create the contructor , unless need to add any special behavior , like adding name in uppercase




@app.route("/")
def index():
    all_data = contact_us.query.all()
    print(all_data)     
    for data in all_data:
        print(data.name)
        print(data.email)
        print(data.message)
    return render_template("index.html")



@app.route("/contact" , methods = ['GET' , 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        msg = request.form.get('msg')

        entry = contact_us(name = name , email=email , message = msg )
        db.session.add(entry)
        db.session.commit()

    all_data = contact_us.query.all()
    return render_template("contact.html",data = all_data)




@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/buy")
def buy():
    return render_template("buy.html")


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

app.run(debug=True)