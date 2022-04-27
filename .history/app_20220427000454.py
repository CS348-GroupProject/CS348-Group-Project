import sqlite3
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import flask_sqlalchemy


app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydata.db'
app.secret_key = "secert_key"
db = SQLAlchemy(app)


user_num = 0
book_num = 0


# Library Model & Functionality
from datetime import datetime
class library(db.Model):
    isbn = db.Column(db.Integer, primary_key=True, nullable=False, index=True)
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

    #db.session.execute('CREATE INDEX isbn_idx ON library(isbn);')

    @app.route('/')
    def show_all():
        return render_template('show_all.html', library_books = library.query.all())

    @app.route('/new', methods = ['GET', 'POST'])
    def new():
        if request.method == 'POST':
            if not request.form['isbn'] or not request.form['title'] or not request.form['author'] or not request.form['genre'] or not request.form['pub_date'] or not request.form['publisher'] or not request.form['total_quantity'] or not request.form['avail_quantity']:
                flash('Please enter all the fields', 'error')
            else:
                new_book = library(int(request.form['isbn']), request.form['title'], request.form['author'], request.form['genre'], datetime.strptime(request.form['pub_date'], '%Y-%m-%d'), request.form['publisher'], int(request.form['total_quantity']), int(request.form['avail_quantity']))

                insert_q = 'INSERT INTO books (isbn, checked_status) VALUES (:inputISBN, 0)'
                params1 = {'inputISBN':request.form['isbn']}

                db.session.execute(insert_q, params1)

                db.session.add(new_book)
                db.session.commit()
                return redirect(url_for('show_all'))
        return render_template('new.html')

    @app.route('/search', methods = ['GET', 'POST'])
    def search():
        if request.method == 'POST':
            if request.form['filters'] == 'ISBN':
                result = db.session.execute('SELECT * FROM library WHERE isbn = :inputISBN', {'inputISBN' : request.form['search']})
                bookFound = []
                for x in result:
                    bookFound.append(tuple(x))
                return render_template('search.html', searchedBooks = bookFound)
            elif request.form['filters'] == 'title':
                result = db.session.execute('SELECT * FROM library WHERE lower(title) = :inputTitle', {'inputTitle' : request.form['search'].lower()})
                bookFound = []
                for x in result:
                    bookFound.append(tuple(x))
                return render_template('search.html', searchedBooks = bookFound)
            elif request.form['filters'] == 'author':
                result = db.session.execute('SELECT * FROM library WHERE lower(author) = :inputAuthor', {'inputAuthor' : request.form['search'].lower()})
                bookFound = []
                for x in result:
                    bookFound.append(tuple(x))
                return render_template('search.html', searchedBooks = bookFound)
            elif request.form['filters'] == 'genre':
                result = db.session.execute('SELECT * FROM library WHERE lower(genre) = :inputGenre', {'inputGenre' : request.form['search'].lower()})
                bookFound = []
                for x in result:
                    bookFound.append(tuple(x))
                return render_template('search.html', searchedBooks = bookFound)
            elif request.form['filters'] == 'publisher':
                result = db.session.execute('SELECT * FROM library WHERE lower(publisher) = :inputPublisher', {'inputPublisher' : request.form['search'].lower()})
                bookFound = []
                for x in result:
                    bookFound.append(tuple(x))
                return render_template('search.html', searchedBooks = bookFound)
        return render_template('search.html')


# Books Model & Functionality
class books(db.Model):
    book_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, index = True)
    isbn = db.Column(db.String(200), nullable=False)
    checked_status = db.Column(db.Boolean, nullable=False)

    #db.session.execute('CREATE INDEX book_id_idx ON books(book_id);')

    def __init__(self, book_id, isbn, checked_status):
        self.book_id = book_id
        self.isbn = isbn
        self.checked_status = checked_status

    @app.route('/show_books')
    def show_books():
        return render_template('show_books.html', books = books.query.all())

    


# Checkout Model & Functionality
class book_checkout(db.Model):
    isbn = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False, index = True)
    date_issued = db.Column(db.DateTime, nullable=False)
    date_due = db.Column(db.DateTime, nullable=False)

    #db.session.execute('CREATE INDEX user_id_idx ON book_checkout(user_id);')

    #constructor
    def __init__(self, isbn, user_id, date_issued, date_due):
        self.isbn = isbn
        self.user_id = user_id
        self.date_issued = date_issued
        self.date_due = date_due
    
    #show all checked 
    @app.route('/show_checked', methods= ['GET', 'POST'])
    def show_checked():
        return render_template('show_checked.html', book_checkout= book_checkout.query.all())

    @app.route('/checkout_book', methods= ['GET', 'POST'])
    def checkout_book():
        if request.method == 'POST':
            if not request.form['isbn'] or not request.form['user_id'] or not request.form['date_issued'] or not request.form['date_due']:
                flash('Cannot Check Out', 'error')
            else:
                has_quantity = db.session.execute('SELECT * FROM library WHERE isbn = :inputISBN', {'inputISBN' : int(request.form['isbn'])}).first()

                if has_quantity != None and has_quantity.available_quantity > 0:
                    check_book = book_checkout(int(request.form['isbn']), int(request.form['user_id']), datetime.strptime(request.form['date_issued'], '%Y-%m-%d'), datetime.strptime(request.form['date_due'], '%Y-%m-%d'))
                    db.session.add(check_book)
                    db.session.execute('UPDATE library SET quantity = quantity - :inputQuantity WHERE isbn = :inputISBN', {'inputISBN' : request.form['isbn'], 'inputQuantity':1})
                    db.session.commit()
                return redirect(url_for('show_checked'))
        return render_template('checkout_book.html')
    
    @app.route('/return_book', methods=['GET', 'POST'])
    def return_book():
        if request.method == 'POST':
            if not request.form['isbn'] or not request.form['user_id']:
                flash('Cannot Return Book', 'error')
            else:
                has_quantity = db.session.execute('SELECT * FROM library WHERE isbn = :inputISBN', {'inputISBN' : request.form['isbn']}).first()

                if has_quantity != None and has_quantity.available_quantity > has_quantity.total_quantity:
                    found_book = book_checkout.query.filter_by(isbn=int(request.form['isbn']), user_id=int(request.form['user_id']))
                    db.session.delete(found_book)
                    db.session.execute('UPDATE library SET quantity = quantity + :inputQuantity WHERE isbn = :inputISBN', {'inputISBN' : request.form['isbn'], 'inputQuantity':1})
                    db.session.commit()
                return redirect(url_for('show_checked'))
        return render_template('return_book.html')

    


# Ordered Books Model & Functionality
from datetime import datetime
class ordered_books(db.Model):

    # isbn is primary key
    isbn = db.Column(db.Integer, primary_key=True, nullable=False, index = True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    eta = db.Column(db.DateTime, nullable=False)
    received = db.Column(db.Boolean, nullable=False)
    genre = db.Column(db.String(200), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False)
    publisher = db.Column(db.String(200), nullable=False)

    # constructor
    def __init__(self, isbn, title, author, quantity, order_date, eta, received, genre, pub_date, publisher):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.quantity = quantity
        self.order_date = order_date
        self.eta = eta
        self.received = received
        self.genre = genre
        self.pub_date = pub_date
        self.publisher = publisher  
    
    #db.session.execute('CREATE INDEX ordered_books_idx ON ordered_books(isbn);')

    # query all ordered books
    @app.route('/show_orders', methods = ['GET', 'POST'])
    def show_orders():
        return render_template('show_orders.html', ordered_books = ordered_books.query.all())
    
    # filter for ordered books based on isbn, author name, or book title
    @app.route('/filter_orders', methods = ['GET', 'POST'])
    def filter_orders():
        if request.method == 'POST':
            res = request.form['filters']
            if res == 'isbn':
                result = db.session.execute('SELECT * FROM ordered_books WHERE isbn = :inputISBN', {'inputISBN' : request.form['search']})
            elif res == 'author':
                result = db.session.execute('SELECT * FROM ordered_books WHERE lower(author) = :inputAuthor', {'inputAuthor' : request.form['search'].lower()})
            elif res == 'title':
                result = db.session.execute('SELECT * FROM ordered_books WHERE lower(title) = :inputTitle', {'inputTitle' : request.form['search'].lower()})
            elif res == 'not received':
                result = db.session.execute('SELECT * FROM ordered_books WHERE received = False')
            elif res == 'received':
                result = db.session.execute('SELECT * FROM ordered_books WHERE received = True')
            return render_template('filter_orders.html', returnOrderedBook = result)
        return render_template('filter_orders.html')
    
    # adding an ordered book to database
    @app.route('/create_order', methods = ['GET', 'POST'])
    def create_order():
        if request.method == 'POST':
            if not request.form['isbn'] or not request.form['title'] or not request.form['author'] or not request.form['quantity'] or not request.form['order_date'] or not request.form['ETA'] or not request.form['genre'] or not request.form['publisher'] or not request.form['pub_date']:
                flash('Cannot add order. Please enter all required fields.', 'error')
            else:
                has_order = db.session.execute('SELECT * FROM ordered_books WHERE isbn = :inputISBN', {'inputISBN' : request.form['isbn']}).first()
                if has_order == None:
                    ordered_book = ordered_books(int(request.form['isbn']), request.form['title'], request.form['author'], int(request.form['quantity']), datetime.strptime(request.form['order_date'], '%Y-%m-%d'), datetime.strptime(request.form['ETA'], '%Y-%m-%d'), False, request.form['genre'], datetime.strptime(request.form['pub_date'], '%Y-%m-%d'), request.form['publisher'])
                    db.session.add(ordered_book)
                    db.session.commit()
                else:
                    flash('There is already an order placed for the given ISBN. Please add to the quantity of the existing order.')
                    return redirect(url_for('modify_existing_order'))
                # return redirect(url_for('show_orders'))
        return render_template('create_order.html')  
    
    # modify the quantity to an existing order
    @app.route('/modify_existing_order', methods=['GET', 'POST'])
    def modify_existing_order():
        if request.method == 'POST':
            if not request.form['isbn'] or not request.form['quantity']:
                flash('Please enter all fields.')
            else:
                update_isbn = request.form['isbn']
                updated_quantity = request.form['quantity']
                db.session.execute('UPDATE ordered_books SET quantity = quantity + :inputQuantity WHERE isbn = :inputISBN', {'inputISBN' : update_isbn, 'inputQuantity':updated_quantity})
                db.session.commit()
                return redirect(url_for('show_orders'))
        return render_template('modify_existing_order.html')
    
    # logging a received ordered book shipment into library inventory and book tables   
    @app.route('/update_order_status', methods=['GET', 'POST'])
    def update_order_status ():
        if request.method == 'POST':
            isbn_add = request.form['isbn']
            res = db.session.execute('SELECT * FROM ordered_books WHERE isbn = :inputISBN AND received = 0', {'inputISBN' : isbn_add}).first()
            if res == None:
                flash('Check ISBN value. The entered ISBN is not present in the orders table')
                return redirect(url_for('update_order_status'))

            else:
                db.session.execute('UPDATE ordered_books SET received = 1 WHERE isbn = :inputISBN', {'inputISBN' : isbn_add})
                # check to see if isbn already exists in library
                in_library = db.session.execute('SELECT isbn FROM library WHERE isbn = :inputISBN', {'inputISBN' : isbn_add}).one_or_none()
                quantity_add = str(res[3])            
                if in_library != None:
                    q = 'UPDATE library SET total_quantity = total_quantity + :quant, available_quantity = available_quantity + :quant WHERE isbn = :inputISBN'
                    params = {'quant': quantity_add, 'inputISBN':isbn_add}
                    db.session.execute(q, params)  
                else:
                    # ordered book is not in the library, so add it 
                    q = 'INSERT INTO library (isbn, title, author, genre, pub_date, publisher, total_quantity, available_quantity) SELECT isbn, title, author, genre, pub_date, publisher, :quant AS total_quantity, :quant AS available_quantity FROM ordered_books WHERE isbn = :inputISBN'
                    params = {'quant': quantity_add, 'inputISBN':isbn_add}
                    db.session.execute(q, params)
                # in either situation, add the new copies to the book table (logs individual copies)
                insert_q = 'INSERT INTO books (isbn, checked_status) VALUES (:inputISBN, 0)'
                params1 = {'inputISBN':isbn_add}
                for i in range(int(quantity_add)):
                    db.session.execute(insert_q, params1)
                db.session.execute('DELETE FROM ordered_books WHERE isbn = :inputISBN', {'inputISBN' : isbn_add})
                db.session.commit()
                return redirect(url_for('show_all'))
        return render_template('update_order_status.html')

# Memberships Model & Functionality
class new_profiles(db.Model):
    user_id = db.Column(db.String(200), primary_key=True, nullable=False, index = True)
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

    #db.session.execute('CREATE INDEX member_idx ON new_profiles(user_id);')

    @app.route('/show_users', methods = ['GET', 'POST'])
    def show_users():
        if request.method == 'POST':
            if request.form['filters'] == 'user id':
                result = db.session.execute('SELECT * FROM new_profiles WHERE user_id = :inputUserID', {'inputUserID' : request.form['search']})
                return render_template('show_users.html', newProfiles = result)

            elif request.form['filters'] == 'first name':
                result = db.session.execute('SELECT * FROM new_profiles WHERE lower(first_name) = :inputFirstName', {'inputFirstName' : request.form['search'].lower()})
                print(result)
                return render_template('show_users.html', newProfiles = result)

            elif request.form['filters'] == 'last name':
                result = db.session.execute('SELECT * FROM new_profiles WHERE lower(last_name) = :inputLastName', {'inputLastName' : request.form['search'].lower()})
                return render_template('show_users.html', newProfiles = result)

            elif request.form['filters'] == 'email add':
                result = db.session.execute('SELECT * FROM new_profiles WHERE lower(email_add) = :inputEmailAdd', {'inputEmailAdd' : request.form['search'].lower()})
                return render_template('show_users.html', newProfiles = result)

            elif request.form['filters'] == 'address':
                result = db.session.execute('SELECT * FROM new_profiles WHERE lower(address) = :inputAdd', {'inputAdd' : request.form['search'].lower()})
                return render_template('show_users.html', newProfiles = result)
            
            elif request.form['filters'] == 'phone no':
                result = db.session.execute('SELECT * FROM new_profiles WHERE phone_no = :inputPhoneNo', {'inputPhoneNo' : request.form['search'].lower()})
                return render_template('show_users.html', newProfiles = result)
        return render_template('show_users.html')

    @app.route('/create_users', methods = ['GET', 'POST'])
    def create_users():
        if request.method == 'POST':
            if not request.form['user_id'] or not request.form['first_name'] or not request.form['last_name'] or not request.form['email_add'] or not request.form['address'] or not request.form['phone_no'] or not request.form['late_fee'] or not request.form['on_waitlist']:
                flash('Please enter all required fields.', 'error')
            else:
                global user_num
                entered_user = new_profiles(request.form['user_id'], request.form['first_name'], request.form['last_name'], request.form['email_add'], request.form['address'], request.form['phone_no'], request.form['late_fee'], request.form['on_waitlist'])
                user_num += 1
                db.session.add(entered_user)
                db.session.commit()
                return redirect(url_for('show_users'))
        return render_template('create_users.html')

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)
