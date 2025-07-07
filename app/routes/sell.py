from flask import Blueprint, render_template, request, session , redirect, url_for, flash
from flask import current_app

from app.models.book import Books
from functools import wraps
from werkzeug.utils import secure_filename
import os



from app import db

sell_bp = Blueprint("sell", __name__)




def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Login required", "warning")
            return redirect(url_for('auth.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function


@sell_bp.route("/buy")
def buy():
    all_books = Books.query.all()
    return render_template("buy.html", books=all_books)

@sell_bp.route("/sell", methods=['GET','POST'])
@login_required
def sell():
    if request.method == "POST":
        title = request.form.get("title")
        price = request.form.get("price")
        year = request.form.get("year")
        book_class = request.form.get("book_class")
        image_file = request.files["image"]

        # Save image
        image_filename = secure_filename(image_file.filename)
        
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')

        #upload_folder = os.path.join("app","static", "uploads") ------------------>>>>>>>>>> this can break when deployed

        image_path = os.path.join(upload_folder, image_filename)
      
        image_file.save(image_path)

        # Create new book
        new_book = Books(
            title=title,
            price=price,
            year=year,
            book_class=book_class,
            image=image_filename,
            user_id=session['user_id']
        )
        db.session.add(new_book)
        db.session.commit()
        flash("Book added successfully!", "success")
        return redirect(url_for('sell.sell'))
    
     # Show books added by this user
    user_books = Books.query.filter_by(user_id=session['user_id']).all()
    return render_template("sell.html", books=user_books)
