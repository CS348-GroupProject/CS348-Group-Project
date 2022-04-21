from lib2to3.pgen2.pgen import generate_grammar
from multiprocessing import AuthenticationError
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from matplotlib.pyplot import title
from matplotlib.style import available
from sqlalchemy import true

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydata.db'
app.secret_key = "secert_key"
db = SQLAlchemy(app)
id = 0

class library(db.model):
    isbn = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    genre = db.Column(db.String(200), nullable=False)
    pub_date
    publisher
    total_quantity
    available_quantity



class books(db.Model):
    book_id = db.Column(db.Integer, primary_key=True, nullable=False)
    isbn = db.Column(db.Integer, nullable=False)
    checked_status = db.Column(db.Boolean, nullable=False)

    def __init__(self, book_id, isbn, checked_status):
        self.book_id = book_id
        self.isbn = isbn
        self.checked_status = checked_status

    @app.route('/')
    def show_all():
        return render_template('show_all.html', books = books.query.all())

    @app.route('/new', methods = ['GET', 'POST'])
    def new():
        if request.method == 'POST':
            if not request.form['isbn'] or not request.form['title'] or not request.form['author']:
                flash('Please enter all the fields', 'error')
            else:
                book = books(id, request.form['isbn'], request.form['title'], request.form['author'])
                id += 1
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
            result = db.session.execute('SELECT book_id, title, author FROM books WHERE isbn = :inputISBN', {'inputISBN' : request.form['search']})
            bookFound = ""
            flag = True
            for x in result:
                if flag:
                    bookFound += x
                    flag = False
                else:
                    bookFound += '\n'
                    bookFound += x
            if (bookFound != ""):
                flash('Book was successfully found!')
            return render_template('search.html', returnBook = bookFound)
        return render_template('search.html')

# Ordered Books Model & Functionality
from datetime import datetime
class ordered_books(db.Model):

    # isbn is primary key
    isbn = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    eta = db.Column(db.DateTime, nullable=False)
    received = db.Column(db.Boolean, nullable=False)

    # constructor
    def __init__(self, isbn, title, author, quantity, order_date, eta, received):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.quantity = quantity
        self.order_date = order_date
        self.eta = eta
        self.received = received
    
    # query all ordered books
    @app.route('/show_orders', methods = ['GET', 'POST'])
    def show_orders():
        return render_template('show_orders.html')
    
    # adding an order
    @app.route('/create_order', methods = ['GET', 'POST'])
    def create_order():
        if request.method == 'POST':
            if not request.form['isbn'] or not request.form['title'] or not request.form['author'] or not request.form['quantity'] or not request.form['order_date'] or not request.form['ETA']:
                flash('Cannot add order. Please enter all required fields.', 'error')
            else:
                ordered_book = ordered_books(request.form['isbn'], request.form['title'], request.form['author'], int(request.form['quantity']), datetime.strptime(request.form['order_date'], '%m/%d/%Y'), datetime.strptime(request.form['ETA'], '%m/%d/%Y'), False)
                db.session.add(ordered_book)
                db.session.commit()
                flash('Book order was submitted successfully.')
                return redirect(url_for('show_orders'))
        return render_template('create_order.html')


class checked_out_books(db.model):
    member_ID = db.Column(db.Integer, nullable=False)
    book_ID = db.Column(db.Integer, primary_key=True, nullable=False)
    issued = db.Column(db.DateTime, nullable=False)
    due = db.Column(db.DateTime, nullable=False)

    def __init__(self, member_ID, book_ID, issued, due):
        self.member_ID = member_ID
        self.book_ID = book_ID
        self.issued = issued
        self.due = due
    
    @app.route('/show_checked', methods = ['GET', 'POST'])
    def show_checked():
        return render_template('show_checked.html')
    
    @app.route('/checkout_book', methods = ['GET', 'POST'])
    def create_order():
        if request.method == 'POST':
            if not request.form['member_ID'] or not request.form['book_ID'] or not request.form['issued'] or not request.form['due']:
                flash('Cannot check out book. Please enter all required fields.', 'error')
            else:
                checked_book = checked_out_books(int(request.form['member_ID']), int(request.form['book_ID']), datetime.strptime(request.form['issued'], '%m/%d/%Y'), datetime.strptime(request.form['due'], '%m/%d/%Y'), False)
                db.session.add(checked_book)
                db.session.commit()
                flash('Book Checked Out successfully.')
                return redirect(url_for('show_checked'))
        return render_template('checkout_book.html')


if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)
