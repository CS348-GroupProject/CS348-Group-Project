from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import flask_sqlalchemy


app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydata.db'
app.secret_key = "secert_key"
db = SQLAlchemy(app)


# Library Model & Functionality
from datetime import datetime
class library(db.Model):
    isbn = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    genre = db.Column(db.String(200), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False)
    publisher = db.Column(db.String(200), nullable=False)
    total_quantity = db.Column(db.Integer, nullable=False)
    available_quantity = db.Column(db.Integer, nullable=True)

    def __init__(self, isbn, title, author, genre, pub_date, publisher, total_quantity, available_quantity):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.genre = genre
        self.pub_date = pub_date
        self.publisher = publisher
        self.total_quantity = total_quantity
        self.available_quantity = available_quantity

    @app.route('/')
    def show_all():
        return render_template('show_all.html', library_books = library.query.all())

    @app.route('/new', methods = ['GET', 'POST'])
    def new():
        if request.method == 'POST':
            if not request.form['isbn'] or not request.form['title'] or not request.form['author'] or not request.form['genre'] or not request.form['pub_date'] or not request.form['publisher'] or not request.form['total_quantity'] or not request.form['avail_quantity']:
                flash('Please enter all the fields', 'error')
            else:
                new_book = library(int(request.form['isbn']), request.form['title'], request.form['author'], request.form['genre'], datetime.strptime(request.form['pub_date'], '%m/%d/%Y'), request.form['publisher'], int(request.form['total_quantity']), int(request.form['avail_quantity']))
                db.session.add(new_book)
                db.session.commit()
                flash('Book was successfully added to the Library!')
                return redirect(url_for('show_all'))
        return render_template('new.html')

    @app.route('/search', methods = ['GET', 'POST'])
    def search():
        if request.method == 'POST':
            flash('Book was successfully found!')
            if request.form['filter'] == 'ISBN':
                result = db.session.execute('SELECT * FROM library WHERE isbn = :inputISBN', {'inputISBN' : request.form['search']})
                bookFound = []
                for x in result:
                    bookFound.append(tuple(x))
                return render_template('search.html', searchedBooks = bookFound)
            elif request.form['filter'] == 'title':
                result = db.session.execute('SELECT * FROM library WHERE lower(title) = :inputTitle', {'inputTitle' : request.form['search'].lower()})
                bookFound = []
                for x in result:
                    bookFound.append(tuple(x))
                return render_template('search.html', searchedBooks = bookFound)
            elif request.form['filter'] == 'author':
                result = db.session.execute('SELECT * FROM library WHERE lower(author) = :inputAuthor', {'inputAuthor' : request.form['search'].lower()})
                bookFound = []
                for x in result:
                    bookFound.append(tuple(x))
                return render_template('search.html', searchedBooks = bookFound)
            elif request.form['filter'] == 'genre':
                result = db.session.execute('SELECT * FROM library WHERE lower(genre) = :inputGenre', {'inputGenre' : request.form['search'].lower()})
                bookFound = []
                for x in result:
                    bookFound.append(tuple(x))
                return render_template('search.html', searchedBooks = bookFound)
            elif request.form['filter'] == 'publisher':
                result = db.session.execute('SELECT * FROM library WHERE lower(publisher) = :inputPublisher', {'inputPublisher' : request.form['search'].lower()})
                bookFound = []
                for x in result:
                    bookFound.append(tuple(x))
                return render_template('search.html', searchedBooks = bookFound)
        return render_template('search.html')


# Books Model & Functionality
class books(db.Model):
    book_id = db.Column(db.Integer, primary_key=True, nullable=False)
    checked_status = db.Column(db.Boolean, nullable=False)
    donated_status = db.Column(db.Boolean, nullable=False)

    def __init__(self, book_id, isbn, donated_status):
        self.book_id = book_id
        self.isbn = isbn
        self.donated_status = donated_status


# Checkout Model & Functionality
class checked_out(db.Model):
    book_id = db.Column(db.Integer, primary_key=True, nullable=False)
    date_issued = db.Column(db.DateTime, nullable=False)
    date_due = db.Column(db.DateTime, nullable=False)

    def __init__(self, book_id, date_issued, date_due):
        self.book_id = book_id
        self.date_issued = date_issued
        self.date_due = date_due


# Ordered Books Model & Functionality
from datetime import datetime
class ordered_books(db.Model):

    # isbn is primary key
    isbn = db.Column(db.String(200), primary_key=True, nullable=False)
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
        return render_template('show_orders.html', ordered_books = ordered_books.query.all())
    
    # filter for ordered books
    @app.route('/filter_orders', methods = ['GET', 'POST'])
    def filter_orders():
        if request.method == 'POST':
            res = request.form['filters']
            if res == 'isbn':
                flash('Book was successfully found!')
                result = db.session.execute('SELECT * FROM ordered_books WHERE isbn = :inputISBN', {'inputISBN' : request.form['search']})
            elif res == 'author':
                flash('Book was successfully found!')
                result = db.session.execute('SELECT * FROM ordered_books WHERE author = :inputAuthor', {'inputAuthor' : request.form['search']})
            elif res == 'title':
                flash('Book was successfully found!')
                result = db.session.execute('SELECT * FROM ordered_books WHERE title = :inputTitle', {'inputTitle' : request.form['search']})
            elif res == 'not received':
                result = db.session.execute('SELECT * FROM ordered_books WHERE received = False')
            elif res == 'received':
                flash('Book is sucessfully found')
                result = db.session.execute('SELECT * FROM ordered_books WHERE received = True')
            return render_template('filter_orders.html', returnOrderedBook = result)

        return render_template('filter_orders.html')
    
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
    
# Memberships Model & Functionality
class new_profiles(db.Model):
    user_id = db.Column(db.String(200), primary_key=True, nullable=False)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    email_add = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    phone_no = db.Column(db.String(500), nullable=False)
    late_fee = db.Column(db.String(200), nullable=False)
    on_waitlist = db.Column(db.String(200), nullable=False)
    

    # constructor
    def __init__(self, user_id, first_name, last_name, email_add, address, phone_no, late_fee, on_waitlist):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email_add = email_add
        self.address = address
        self.phone_no = phone_no
        self.late_fee = late_fee
        self.on_waitlist = on_waitlist

    @app.route('/show_users', methods = ['GET', 'POST'])
    def show_users():
        return render_template('show_users.html', new_profiles = new_profiles.query.all())

    @app.route('/create_users', methods = ['GET', 'POST'])
    def create_users():
        if request.method == 'POST':
            if not request.form['user_id'] or not request.form['first_name'] or not request.form['last_name'] or not request.form['email_add'] or not request.form['address'] or not request.form['phone_no'] or not request.form['late_fee'] or not request.form['on_waitlist']:
                flash('Please enter all required fields.', 'error')
            else:
                entered_user = new_profiles(request.form['user_id'], request.form['first_name'], request.form['last_name'], request.form['email_add'], request.form['address'], request.form['phone_no'], request.form['late_fee'], request.form['on_waitlist'])
                db.session.add(entered_user)
                db.session.commit()
                flash('New profile was added successfully!')
                return redirect(url_for('show_users'))
        return render_template('create_users.html')

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)
