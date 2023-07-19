from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book-shelf.db'
db = SQLAlchemy()
db.init_app(app=app)


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
    return render_template('add.html')


if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True)

