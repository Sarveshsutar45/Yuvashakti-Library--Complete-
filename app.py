from datetime import datetime, timedelta
from flask_mail import Mail, Message
from flask import Flask, flash, jsonify,  redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

# Automatically load variables from .env file
load_dotenv()

app = Flask(__name__, static_url_path='/static')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'library'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.secret_key = 'j8KsT6hRnLmP5qBv'

mail = Mail(app)
mysql = MySQL(app)


@app.route('/',  methods=['GET'])
@app.route('/home',  methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/send_email', methods=['POST'])
def send_email():
    recipient_email = request.form['email']
    subject = request.form['subject']
    message_body = request.form['message']

    msg = Message(subject=subject, sender=app.config['MAIL_USERNAME'], recipients=[
                  recipient_email])
    msg.body = message_body

    mail.send(msg)

    return 'Email Sent!'


@app.route('/about',  methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'admin' in session:
        return redirect(url_for('dash'))
    elif 'user_id' in session:
        return redirect(url_for('books'))

    if request.method == 'POST':
        FullName = request.form['FullName']
        Username = request.form['Username']
        Email = request.form['Email']
        Password = request.form['Password']
        cur = mysql.connection.cursor()

        # check if username or email already exists
        cur.execute(
            "SELECT * FROM users WHERE Username = %s OR Email = %s", (Username, Email))
        mysql.connection.commit()
        user = cur.fetchone()

        if user:
            return render_template('log_reg.html', error='User already exists')

        cur.execute("INSERT INTO users (FullName,Username, Email, Password) VALUES (%s, %s, %s, %s)",
                    (FullName, Username, Email, Password))
        mysql.connection.commit()
        user_id = cur.lastrowid

        # insert into activity table
        cur.execute("INSERT INTO activity (username, reg_date) VALUES (%s, %s)",
                    (Username, datetime.now()))
        mysql.connection.commit()
        cur.close()

        # save username in session
        session['username'] = Username
        # save user id in session
        session['user_id'] = user_id
        # send user to books page
        return redirect(url_for('books'))
        # return 'Registered successfully!  Go to <a href="/">Home</a>'
    return render_template('log_reg.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'admin' in session:
        return redirect(url_for('dash'))
    elif 'user_id' in session:
        return redirect(url_for('books'))

    if request.method == 'POST':
        Username = request.form['Username']
        Password = request.form['Password']
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM users WHERE Username = %s AND Password = %s", (Username, Password))
        mysql.connection.commit()
        user = cur.fetchone()
        if user:
            # save username in session
            session['username'] = user[2]
            session['user_id'] = user[0]

            # insert into activity table
            cur.execute("INSERT INTO activity (username, last_login) VALUES (%s, %s)",
                        (user[2], datetime.now()))
            mysql.connection.commit()
            cur.close()

            return redirect(url_for('books'))
        else:
            return render_template('log_reg.html', error='Invalid username or password')
    return render_template('log_reg.html')


@app.route('/gallery', methods=['GET'])
def gallery():
    return render_template('gallery.html')


@app.route('/logout', methods=['GET'])
def logout():
    if 'admin' not in session:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO activity (username, logout) VALUES (%s, %s)",
                    (session['username'], datetime.now()))
        mysql.connection.commit()
        cur.close()
    session.pop('username', None)
    session.pop('user_id', None)
    session.pop('admin', None)
    return redirect(url_for('home'))


@app.route('/books',  methods=['GET'])
def books():
    # check if user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    books = []
    cursor.execute("SELECT * FROM books")
    mysql.connection.commit()
    result = cursor.fetchall()
    books = []
    for row in result:
        book = {
            'name': row[1],
            'publisher': row[2],
            'book_id': row[3],
            'category': row[4],
            'author': row[5],
            'copies_available': row[6],
            'price': row[7],
            'status': row[8],
            'added_on': row[9]
        }
        books.append(book)
        admin = False
        if 'admin' in session:
            admin = session['admin']
    return render_template('books.html', books=books, admin=admin, username=session['username'])


@app.route('/borrows', methods=['GET'])
def borrows():
    # check if user is logged in
    if 'admin' not in session:
        return redirect(url_for('admin'))

    cursor = mysql.connection.cursor()
    borrows = []
    # get all from user_books table where submitted_date is null
    cursor.execute(
        "SELECT ub.user_id, ub.book_id, ub.borrow_date, ub.return_date, b.name, b.publisher, b.category, b.author, u.fullname FROM user_books ub JOIN books b ON ub.book_id=b.book_id JOIN users u ON ub.user_id=u.id WHERE ub.submitted_date IS NULL")
    mysql.connection.commit()
    result = cursor.fetchall()
    borrows = []
    for row in result:
        borrow = {
            'user_id': row[0],
            'book_id': row[1],
            'borrow_date': row[2],
            'return_date': row[3],
            'book_name': row[4],
            'publisher': row[5],
            'category': row[6],
            'author': row[7],
            'fullname': row[8]
        }
        borrows.append(borrow)

    return render_template('borrows.html', books=borrows, username=session['username'])


@app.route('/returns', methods=['GET'])
def returns():
    # check if user is logged in
    if 'admin' not in session:
        return redirect(url_for('admin'))

    cursor = mysql.connection.cursor()
    borrows = []
    # get all from user_books table where submitted_date is null
    cursor.execute(
        "SELECT ub.user_id, ub.book_id, ub.borrow_date, ub.return_date, ub.submitted_date, b.name, b.publisher, b.category, b.author, u.fullname FROM user_books ub JOIN books b ON ub.book_id=b.book_id JOIN users u ON ub.user_id=u.id WHERE ub.submitted_date IS NOT NULL")
    mysql.connection.commit()
    result = cursor.fetchall()
    borrows = []
    for row in result:
        borrow = {
            'user_id': row[0],
            'book_id': row[1],
            'borrow_date': row[2],
            'return_date': row[3],
            'submitted_date': row[4],
            'book_name': row[5],
            'publisher': row[6],
            'category': row[7],
            'author': row[8],
            'fullname': row[9]
        }
        borrows.append(borrow)

    return render_template('returns.html', books=borrows, username=session['username'])


@app.route('/my-books', methods=['GET'])
def my_books():
    # check if user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    books = []
    # select every book of that user id FROM user_books table
    user_id = session['user_id']
    cursor.execute("SELECT b.publisher, b.name, b.book_id, b.category, b.author, ub.borrow_date, ub.return_date, ub.submitted_date FROM user_books ub JOIN books b ON ub.book_id=b.book_id WHERE ub.user_id= % s", (user_id,))
    mysql.connection.commit()
    result = cursor.fetchall()
    books = []
    for index, row in enumerate(result):
        book = {
            'id': index+1,
            'publisher': row[0],
            'name': row[1],
            'book_id': row[2],
            'category': row[3],
            'author': row[4],
            'borrow_date': row[5].strftime('%d-%m-%y'),
            'return_date': row[6].strftime('%d-%m-%y'),
            'submitted_date': '-' if row[7] is None else row[7].strftime('%d-%m-%y')
        }
        books.append(book)
    return render_template('books.html', books=books, username=session['username'])


@app.route('/borrow-books/<int:id>', methods=['GET'])
def borrow_books(id):
    if 'admin' not in session:
        return redirect(url_for('admin'))

    user_id = id
    cur = mysql.connection.cursor()

    # fetch full name of user
    cur.execute("SELECT FullName FROM users WHERE id = %s", (user_id,))
    mysql.connection.commit()
    user_name = cur.fetchone()[0]

    # fetch books with copies available
    cur.execute("SELECT * FROM books WHERE copies_available > 0")
    rows = cur.fetchall()

    books = []

    # filter books based on user_books table
    for row in rows:
        cur.execute(
            "SELECT * FROM user_books WHERE user_id = %s AND book_id = %s AND submitted_date IS NULL", (user_id, row[3]))
        user_book_row = cur.fetchone()
        if not user_book_row:
            books.append({
                'id': row[0],
                'name': row[1],
                'book_id': row[3],
                'category': row[4],
                'author': row[5],
                'status': row[8],
            })

    cur.close()
    return render_template('borrow_books.html', user_name=user_name, user_id=id, books=books, username=session['username'])


@app.route('/borrow/<int:id>', methods=['POST'])
def borrow(id):
    books = request.form
    cursor = mysql.connection.cursor()
    user_id = id
    borrow_date = datetime.now()
    return_date = (datetime.now() +
                   timedelta(days=7))
    for book_id in books:
        cursor.execute("INSERT INTO user_books (user_id, book_id, borrow_date, return_date) VALUES (%s, %s, %s, %s)",
                       (user_id, book_id, borrow_date, return_date))
        mysql.connection.commit()

        # get username of the user
        cursor.execute("SELECT username FROM users WHERE id = %s", (user_id,))
        mysql.connection.commit()
        username = cursor.fetchone()[0]

        # get book name of the book
        cursor.execute("SELECT name FROM books WHERE book_id = %s", (book_id,))
        mysql.connection.commit()
        book_name = cursor.fetchone()[0]

        cursor.execute("INSERT INTO activity (username, book_name, borrow_date) VALUES (%s, %s, %s)",
                       (username, book_name, borrow_date))
        mysql.connection.commit()

        # update the copies_available field in the books table by increasing it by 1
        cursor.execute(
            "UPDATE books SET copies_available = copies_available - 1 WHERE book_id = %s", (book_id,))
        mysql.connection.commit()

        # check if quantity is 0, if yes, update the status to 'Unavailable'
        cursor.execute(
            "SELECT copies_available FROM books WHERE book_id = %s", (book_id,))
        mysql.connection.commit()
        copies_available = cursor.fetchone()[0]
        if copies_available == 0:
            cursor.execute(
                "UPDATE books SET status = 'Unavailable' WHERE book_id = %s", (book_id,))
            mysql.connection.commit()
    response_data = {'message': 'Books borrowed'}
    return jsonify(response_data), 200


@app.route('/return', methods=['POST'])
def return_book():
    cursor = mysql.connection.cursor()
    # get the book_id from the request data
    book_id = request.form['book_id']
    user_id = request.form['user_id']

    # update date
    date = datetime.now()

    # construct the update query
    update_query = "UPDATE user_books SET submitted_date = %s WHERE book_id = %s and user_id = %s;"

    # add the activity to the activity table
    cursor.execute("SELECT username FROM users WHERE id = %s", (user_id,))
    mysql.connection.commit()
    username = cursor.fetchone()[0]

    # get book name of the book
    cursor.execute("SELECT name FROM books WHERE book_id = %s", (book_id,))
    mysql.connection.commit()
    book_name = cursor.fetchone()[0]

    cursor.execute("INSERT INTO activity (username, book_name, return_date) VALUES (%s, %s, %s)",
                   (username, book_name, date))
    mysql.connection.commit()

    # execute the update query
    cursor.execute(update_query, (date, book_id, user_id))
    mysql.connection.commit()

    # update the copies_available field in the books table by increasing it by 1
    cursor.execute(
        "UPDATE books SET copies_available = copies_available + 1 WHERE book_id = %s", (book_id,))

    mysql.connection.commit()

    # check if quantity is 1, if yes, update the status to 'Available'
    cursor.execute(
        "SELECT * FROM books WHERE book_id = %s AND copies_available = 1", (book_id,))
    mysql.connection.commit()
    result = cursor.fetchone()
    if result:
        cursor.execute(
            "UPDATE books SET status = 'Available' WHERE book_id = %s", (book_id,))
        mysql.connection.commit()

    return 'Book returned successfully!'


@app.route('/admin',  methods=['GET'])
def admin():
    return render_template('admin.html')


@app.route('/login_admin',  methods=['POST'])
def login_admin():
    Username = request.form['Username']
    Password = request.form['Password']

    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT * FROM admin WHERE Username = %s AND Password = %s", (Username, Password))
    result = cursor.fetchone()
    mysql.connection.commit()
    cursor.close()

    if result:
        session['username'] = Username
        session['admin'] = True
        return redirect(url_for('dash'))
    else:
        return redirect(url_for('login'))


@app.route('/dashboard',  methods=['GET'])
def dash():
    if 'admin' not in session:
        return redirect(url_for('admin'))

    cursor = mysql.connection.cursor()
    cursor.execute(
        'SELECT * FROM activity ORDER BY id DESC LIMIT 15 OFFSET 0;')
    activity_data = cursor.fetchall()

    activity_list = []

    for row in activity_data:
        row_dict = {}
        for i, column_name in enumerate(cursor.description):
            row_dict[column_name[0]] = row[i]
        activity_list.append(row_dict)

    # get count of all copies_available from book table
    cursor.execute('SELECT SUM(copies_available) FROM books')
    book_copies_count = cursor.fetchone()[0]

    # get book count
    cursor.execute('SELECT COUNT(*) FROM books')
    book_count = cursor.fetchone()[0]

    # get user count
    cursor.execute('SELECT COUNT(*) FROM users')
    user_count = cursor.fetchone()[0]

    # get user_books count
    cursor.execute(
        'SELECT COUNT(*) FROM user_books WHERE submitted_date IS NULL')
    borrowed_count = cursor.fetchone()[0]

    # Render the dashboard template with the activity data
    return render_template('dash.html', activity_data=activity_list, book_count=book_count, user_count=user_count, borrowed_count=borrowed_count, book_copies_count=book_copies_count)


@app.route('/addbook', methods=['GET', 'POST'])
def addbook():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    if request.method == 'POST':
        book_id = request.form['book_id']
        name = request.form['name']
        category = request.form['category']
        author = request.form['author']
        publisher = request.form['publisher']
        copies_available = request.form['copies_available']
        price = request.form['price']
        status = request.form['status']
        added_on = request.form['added_on']
        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO books (book_id, name, category, author, publisher, copies_available, price, status, added_on) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (book_id, name, category, author, publisher, copies_available, price, status, added_on))
            mysql.connection.commit()
            flash("Book added successfully!")
            return redirect(url_for('addbook'))
        except:
            flash("Book ID already exists!")
            return redirect(url_for('addbook'))
        cur.close()

        return redirect(url_for('books'))
    return render_template('addbook.html')


@app.route('/users', methods=['GET'])
def users():
    # check if user is logged in
    if 'admin' not in session:
        return redirect(url_for('admin'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users")
    mysql.connection.commit()
    result = cursor.fetchall()
    users = []
    for row in result:
        user = {
            'id': row[0],
            'name': row[1],
            'username': row[2],
            'email': row[3],
            'reg_on': row[5],
        }
        users.append(user)
    cursor.close()
    return render_template('users.html', users=users, admin=True)


@app.route('/user-details/<int:id>', methods=['GET'])
def user_details(id):
    if 'admin' not in session:
        return redirect(url_for('admin'))
    cursor = mysql.connection.cursor()
   # query to get the user details
    query = """
    SELECT users.FullName, users.email, user_books.user_id, books.book_id, user_books.borrow_date, user_books.return_date, books.name, user_books.submitted_date
    FROM users
    JOIN user_books ON users.id = user_books.user_id
    JOIN books ON books.book_id = user_books.book_id
    WHERE users.id = %s
    """
    cursor.execute(query, (id,))
    rows = cursor.fetchall()

    # map the fetched data to the desired format
    user_books = []
    name = ''
    for index, row in enumerate(reversed(rows)):
        name = row[0]
        email = row[1]
        user_books.append({
            'id': len(rows) - index,
            'book_id': row[3],
            'borrow_date': row[4],
            'due_date': row[5],
            'book_name': row[6],
            'submitted_date': row[7]
        })
    not_return = len(
        [book for book in user_books if book['submitted_date'] is None])

    return render_template('user_details.html', name=name, email=email, not_return=not_return, user_id=id, books=user_books,  admin=True)


@app.route('/book-details/<int:id>', methods=['GET'])
def book_details(id):
    if 'admin' not in session:
        return redirect(url_for('admin'))
    cursor = mysql.connection.cursor()
    book_name = ''
    user_books = []
    try:
        query = """
        SELECT users.FullName, users.id, user_books.book_id, books.name, books.category, user_books.borrow_date, user_books.return_date, user_books.submitted_date
        FROM users
        JOIN user_books ON users.id = user_books.user_id
        JOIN books ON books.book_id = user_books.book_id
        WHERE user_books.book_id = %s
        """
        cursor.execute(query, (id,))
        rows = cursor.fetchall()
        print(rows)
        if len(rows) > 0:
            for row in reversed(rows):
                book_name = row[3]
                user_books.append({
                    'name': row[0],
                    'user_id': row[1],
                    'book_id': row[2],
                    'borrow_date': row[5],
                    'due_date': row[6],
                    'submitted_date': row[7]
                })
        else:
            # get the book details
            cursor.execute("SELECT * FROM books WHERE book_id = %s", (id,))
            mysql.connection.commit()
            result = cursor.fetchone()
            book_name = result[1]
            cursor.close()
    except Exception as e:
        print('error', e)
    return render_template('book_details.html', book_name=book_name, users=user_books, admin=True)

    # return render_template('book_details.html', book_id=id, users=user_books, admin=True)


@app.route('/reports', methods=['GET', 'POST'])
def reports():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    if request.method == 'POST':
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        # desired data - user_count, book_count, books_borrowed_count, books_returned_count, copies_count, activity_count
        # where date is between from_date and to_date
        cursor = mysql.connection.cursor()
        # first query to get the user_count
        query = "SELECT COUNT(*) FROM users WHERE reg_on BETWEEN %s AND %s"
        cursor.execute(query, (from_date, to_date))
        result = cursor.fetchone()
        user_count = result[0]

        query = "SELECT * FROM users WHERE reg_on BETWEEN %s AND %s"
        cursor.execute(query, (from_date, to_date))
        result = cursor.fetchall()
        users = []
        for row in result:
            user = {
                'id': row[0],
                'name': row[1],
                'username': row[2],
                'email': row[3],
                'reg_on': row[5],
            }
            users.append(user)

        # second query to get the book_count
        query = "SELECT COUNT(*) FROM books WHERE added_on BETWEEN %s AND %s"
        cursor.execute(query, (from_date, to_date))
        book_count = cursor.fetchone()[0]

        query = "SELECT * FROM books WHERE added_on BETWEEN %s AND %s"
        cursor.execute(query, (from_date, to_date))
        result = cursor.fetchall()
        books = []
        for row in result:
            book = {
                'name': row[1],
                'publisher': row[2],
                'book_id': row[3],
                'category': row[4],
                'author': row[5],
                'copies_available': row[6],
                'price': row[7],
                'status': row[8],
                'added_on': row[9]
            }
            books.append(book)

        # third query to get the books_borrowed_count
        query = "SELECT COUNT(*) FROM user_books WHERE borrow_date BETWEEN %s AND %s"
        cursor.execute(query, (from_date, to_date))
        books_borrowed_count = cursor.fetchone()[0]

        query = """
        SELECT ub.user_id, ub.book_id, ub.borrow_date, ub.return_date, b.name, b.publisher, b.category, b.author, u.fullname 
        FROM user_books ub 
        JOIN books b ON ub.book_id = b.book_id 
        JOIN users u ON ub.user_id = u.id 
        WHERE ub.submitted_date IS NULL 
        AND ub.borrow_date BETWEEN %s AND %s
        """
        cursor.execute(query, (from_date, to_date))
        result = cursor.fetchall()
        borrrowed = []
        for row in result:
            borrow = {
                'user_id': row[0],
                'book_id': row[1],
                'borrow_date': row[2],
                'return_date': row[3],
                'book_name': row[4],
                'publisher': row[5],
                'category': row[6],
                'author': row[7],
                'fullname': row[8]
            }
            borrrowed.append(borrow)

        # fourth query to get the books_returned_count
        query = "SELECT COUNT(*) FROM user_books WHERE submitted_date BETWEEN %s AND %s"
        cursor.execute(query, (from_date, to_date))
        books_returned_count = cursor.fetchone()[0]

        cursor.execute(
            "SELECT ub.user_id, ub.book_id, ub.borrow_date, ub.return_date, ub.submitted_date, b.name, b.publisher, b.category, b.author, u.fullname FROM user_books ub JOIN books b ON ub.book_id=b.book_id JOIN users u ON ub.user_id=u.id WHERE ub.submitted_date IS NOT NULL AND ub.borrow_date BETWEEN %s AND %s", (from_date, to_date))
        result = cursor.fetchall()
        returned = []
        for row in result:
            borrow = {
                'user_id': row[0],
                'book_id': row[1],
                'borrow_date': row[2],
                'return_date': row[3],
                'submitted_date': row[4],
                'book_name': row[5],
                'publisher': row[6],
                'category': row[7],
                'author': row[8],
                'fullname': row[9]
            }
            returned.append(borrow)

        # fifth query to get the copies_count
        query = "SELECT SUM(copies_available) FROM books WHERE added_on BETWEEN %s AND %s"
        cursor.execute(query, (from_date, to_date))
        copies_count = cursor.fetchone()[0]
        if copies_count is None:
            copies_count = 0

        # sixth query to get the activity_count
        query = """SELECT COUNT(*) FROM activity 
        WHERE 
        borrow_date BETWEEN %s AND %s
        OR
        return_date BETWEEN %s AND %s
        OR 
        last_login BETWEEN %s AND %s
        OR
        reg_date BETWEEN %s AND %s
        OR
        logout BETWEEN %s AND %s
        """
        cursor.execute(query, (from_date, to_date, from_date, to_date,
                       from_date, to_date, from_date, to_date, from_date, to_date))
        activity_count = cursor.fetchone()[0]

        query = """
        SELECT * FROM activity
        WHERE 
            (borrow_date BETWEEN %s AND %s)
            OR (return_date BETWEEN %s AND %s)
            OR (last_login BETWEEN %s AND %s)
            OR (reg_date BETWEEN %s AND %s)
            OR (logout BETWEEN %s AND %s)
        """
        cursor.execute(query, (from_date, to_date, from_date, to_date,
                       from_date, to_date, from_date, to_date, from_date, to_date))
        rows = cursor.fetchall()
        # map the fetched data to the desired format
        users_activity = []
        for index, row in enumerate(reversed(rows)):
            username = row[1]
            # get id, fullname from users table
            query = "SELECT id, FullName FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            user_id = result[0]
            fullname = result[1]
            activity = ''
            date = ''
            if row[3] != None:
                activity = 'borrowed ' + row[2]
                date = row[3]
            elif row[4] != None:
                activity = 'returned ' + row[2]
                date = row[4]
            elif row[5] != None:
                activity = 'logged in'
                date = row[5]
            elif row[6] != None:
                activity = 'registered'
                date = row[6]
            elif row[7] != None:
                activity = 'logged out'
                date = row[7]
            users_activity.append({
                'id': len(rows) - index,
                'user_id': user_id,
                'username': username,
                'name': fullname,
                'activity': activity,
                'date': date
            })
        cursor.close()
        result = {
            'user_count': user_count,
            'book_count': book_count,
            'books_borrowed_count': books_borrowed_count,
            'books_returned_count': books_returned_count,
            'copies_count': copies_count,
            'activity_count': activity_count,
            'activities': users_activity,
            'books': books,
            'users': users,
            'returned': returned,
            'borrowed': borrrowed
        }
        # return in json format
        return jsonify(result)
    return render_template('reports.html', admin=True)


@app.route('/users-activity', methods=['GET'])
def users_activity():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    cursor = mysql.connection.cursor()
    # query to get the user details
    query = "SELECT * FROM activity"
    cursor.execute(query)
    rows = cursor.fetchall()
    # map the fetched data to the desired format
    users_activity = []
    for index, row in enumerate(reversed(rows)):
        username = row[1]
        # get id, fullname from users table
        query = "SELECT id, FullName FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        user_id = result[0]
        fullname = result[1]
        activity = ''
        date = ''
        if row[3] != None:
            activity = 'borrowed ' + row[2]
            date = row[3]
        elif row[4] != None:
            activity = 'returned ' + row[2]
            date = row[4]
        elif row[5] != None:
            activity = 'logged in'
            date = row[5]
        elif row[6] != None:
            activity = 'registered'
            date = row[6]
        elif row[7] != None:
            activity = 'logged out'
            date = row[7]
        users_activity.append({
            'id': len(rows) - index,
            'user_id': user_id,
            'username': username,
            'name': fullname,
            'activity': activity,
            'date': date
        })
    return render_template('user_activity.html', activities=users_activity, admin=True)


if __name__ == '__main__':
    app.run(debug=True)
