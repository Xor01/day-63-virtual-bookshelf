from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from os import getenv
from dotenv import load_dotenv
from book import Book, db
from book_form import BookForm
app = Flask(__name__)
app.secret_key = getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book-shelf.db'
db.init_app(app=app)
Bootstrap5(app=app)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    with app.app_context():
        books = Book.query.all()
    return render_template('index.html', books=books)


@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        book = {
            'title': request.form.get('title'),
            'author': request.form.get('author'),
            'rating': request.form.get('rating')
        }
        book_to_add = Book(title=book['title'], author=book['author'], rating=book['rating'])
        try:
            with app.app_context():
                db.session.add(book_to_add)
                db.session.commit()
            return redirect(url_for('home'))
        except Exception as e:
            print(e)
    return render_template('add.html')


@app.route('/edit/<int:book_id>')
def edit(book_id):
    book = db.get_or_404(Book, book_id)
    form = BookForm()
    return render_template('edit.html', book=book, form=form)


if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True)
