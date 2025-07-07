from app import db
from datetime import datetime

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
