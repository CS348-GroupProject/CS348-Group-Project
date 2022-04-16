from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydata.db'
app.secret_key = "secert_key"
db = SQLAlchemy(app)

class books(db.Model):
    isbn = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))

    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self.title = title
        self.author = author

    @app.route('/')
    def show_all():
        return render_template('show_all.html', books = books.query.all() )

    @app.route('/new', methods = ['GET', 'POST'])
    def new():
        if request.method == 'POST':
            if not request.form['isbn'] or not request.form['title'] or not request.form['author']:
                flash('Please enter all the fields', 'error')
            else:
                book = books(request.form['isbn'], request.form['title'], request.form['author'])
                #db.session.delete(books.query.get_or_404(1234567))  USE THIS STATEMENT TO DELETE ANY DUMMY BOOK DATA
                db.session.add(book)
                db.session.commit()
                flash('Book was successfully added!')
                return redirect(url_for('show_all'))
        return render_template('new.html')

    @app.route('/search', methods = ['GET', 'POST'])
    def search():
        if request.method == 'POST':
            flash('Book was successfully found!')
            return render_template('search.html', sTitle = books.query.get_or_404(request.form['search']).title, sAuthor = books.query.get_or_404(request.form['search']).author)
        return render_template('search.html')
if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)
