from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book-shelf.db'
db = SQLAlchemy()
db.init_app(app=app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


@app.route('/')
def home():
    return render_template('index.html')


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


if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True)
