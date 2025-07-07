from app import db

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    book_class = db.Column(db.String(20), nullable=False)  # e.g. Class 10, 12
    image = db.Column(db.String(200))  # store image path (uploaded to /static/uploads)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    seller = db.relationship('Users', backref=db.backref('books', lazy=True))
