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
        if request.form.get('cancel'):
            return redirect(url_for('home'))
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
    form = BookForm()
    return render_template('add.html', form=form)


@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit(book_id):
    book = db.get_or_404(Book, book_id)
    form = BookForm()
    if request.method == 'POST':
        try:
            with app.app_context():
                book_to_update = db.get_or_404(Book, book_id)
                book_to_update.title = request.form.get('title')
                book_to_update.author = request.form.get('author')
                book_to_update.rating = request.form.get('rating')
                db.session.commit()
                return redirect(url_for('home'))
        except Exception as e:
            print(e)
    return render_template('edit.html', book=book, form=form)


@app.route('/delete/<int:book_id>', methods=['POST', 'GET'])
def delete(book_id):
    book = db.get_or_404(Book, book_id)
    form = BookForm()
    if request.method == 'POST':
        if request.form.get('cancel'):
            return redirect(url_for('home'))
        if request.form.get('submit'):
            with app.app_context():
                try:
                    book_to_delete = db.get_or_404(Book, book_id)
                    db.session.delete(book_to_delete)
                    db.session.commit()
                    return redirect(url_for('home'))
                except Exception as e:
                    print(e)
    return render_template('delete.html', book=book, form=form)


if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True)
