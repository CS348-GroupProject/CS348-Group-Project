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
        return render_template('show_all.html', books = books.query.all())

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
            result = db.session.execute('SELECT title, author FROM books WHERE isbn = :inputISBN', {'inputISBN' : request.form['search']})
            bookFound = ""
            for x in result:
                bookFound = x
            return render_template('search.html', returnBook = bookFound)
        return render_template('search.html')

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
    
# create and view new profiles
class new_profiles(db.Model):
    user_id = db.Column(db.String(200), primary_key=True, nullable=False)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(500), nullable=False)

    # constructor
    def __init__(self, user_id, first_name, last_name, address):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address

    @app.route('/show_users', methods = ['GET', 'POST'])
    def show_users():
        return render_template('show_users.html')

    @app.route('/create_users', methods = ['GET', 'POST'])
    def create_users():
        if request.method == 'POST':
            if not request.form['user_id'] or not request.form['first_name'] or not request.form['last_name'] or not request.form['address']:
                flash('Please enter all required fields.', 'error')
            else:
                entered_user = new_profiles(request.form['user_id'], request.form['first_name'], request.form['last_name'], request.form['address'])
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
