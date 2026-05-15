from flask import Flask, render_template, request, redirect, session
import mysql.connector
import time

app = Flask(__name__)

app.secret_key = 'librarysecret'

connection = None

while connection is None:

    try:

        connection = mysql.connector.connect(
            host='library_mysql',
            user='root',
            password='NewPassword123',
            database='librarydb'
        )

        print('MySQL Connected')

    except:

        print('Waiting for MySQL...')
        time.sleep(5)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/loginuser', methods=['POST'])
def loginuser():

    email = request.form['email']
    password = request.form['password']

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        '''
        SELECT * FROM users
        WHERE email=%s
        AND password=%s
        AND role='admin'
        ''',
        (email,password)
    )

    user = cursor.fetchone()

    if user:

        session['user'] = user['name']
        session['role'] = user['role']
        session['id'] = user['id']

        return redirect('/dashboard')

    return 'Only Admin Login Allowed'

@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect('/login')

    cursor = connection.cursor()

    cursor.execute('SELECT COUNT(*) FROM books')
    total_books = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM users WHERE role="user"')
    total_users = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM borrow_books')
    borrowed_books = cursor.fetchone()[0]

    return render_template(
        'dashboard.html',
        total_books=total_books,
        total_users=total_users,
        borrowed_books=borrowed_books,
        username=session['user']
    )

@app.route('/books')
def books():

    cursor = connection.cursor(dictionary=True)

    cursor.execute('SELECT * FROM books')

    books = cursor.fetchall()

    cursor.execute(
        'SELECT * FROM users WHERE role="user"'
    )

    users = cursor.fetchall()

    return render_template(
        'books.html',
        books=books,
        users=users
    )

@app.route('/addbook')
def addbook():

    return render_template('addbook.html')

@app.route('/add', methods=['POST'])
def add():

    title = request.form['title']
    author = request.form['author']
    category = request.form['category']
    quantity = request.form['quantity']

    cursor = connection.cursor()

    cursor.execute(
        '''
        INSERT INTO books
        (title,author,category,quantity,available)

        VALUES(%s,%s,%s,%s,%s)
        ''',
        (
            title,
            author,
            category,
            quantity,
            quantity
        )
    )

    connection.commit()

    return redirect('/books')

@app.route('/deletebook/<int:id>')
def deletebook(id):

    cursor = connection.cursor()

    cursor.execute(
        'DELETE FROM books WHERE id=%s',
        (id,)
    )

    connection.commit()

    return redirect('/books')

@app.route('/users')
def users():

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        'SELECT * FROM users WHERE role="user"'
    )

    users = cursor.fetchall()

    return render_template(
        'users.html',
        users=users
    )

@app.route('/adduser', methods=['POST'])
def adduser():

    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    usn = request.form['usn']
    department = request.form['department']
    password = request.form['password']

    cursor = connection.cursor()

    cursor.execute(
        '''
        INSERT INTO users
        (name,email,phone,usn,department,password,role)

        VALUES(%s,%s,%s,%s,%s,%s,%s)
        ''',
        (
            name,
            email,
            phone,
            usn,
            department,
            password,
            'user'
        )
    )

    connection.commit()

    return redirect('/users')

@app.route('/deleteuser/<int:id>')
def deleteuser(id):

    cursor = connection.cursor()

    cursor.execute(
        'DELETE FROM users WHERE id=%s',
        (id,)
    )

    connection.commit()

    return redirect('/users')

@app.route('/allocate/<int:book_id>/<int:user_id>')
def allocate(book_id,user_id):

    cursor = connection.cursor()

    cursor.execute(
        '''
        SELECT available
        FROM books
        WHERE id=%s
        ''',
        (book_id,)
    )

    available = cursor.fetchone()[0]

    if available > 0:

        cursor.execute(
            '''
            INSERT INTO borrow_books
            (user_id,book_id,issue_date,status)

            VALUES(%s,%s,CURDATE(),%s)
            ''',
            (
                user_id,
                book_id,
                'Borrowed'
            )
        )

        cursor.execute(
            '''
            UPDATE books
            SET available=available-1
            WHERE id=%s
            ''',
            (book_id,)
        )

        connection.commit()

    return redirect('/allocatedbooks')

@app.route('/allocatedbooks')
def allocatedbooks():

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        '''
        SELECT
        borrow_books.id,
        users.name,
        users.usn,
        books.title,
        books.author,
        borrow_books.issue_date

        FROM borrow_books

        JOIN users
        ON borrow_books.user_id = users.id

        JOIN books
        ON borrow_books.book_id = books.id
        '''
    )

    books = cursor.fetchall()

    return render_template(
        'allocatedbooks.html',
        books=books
    )

@app.route('/returnbook/<int:id>')
def returnbook(id):

    cursor = connection.cursor()

    cursor.execute(
        '''
        SELECT book_id
        FROM borrow_books
        WHERE id=%s
        ''',
        (id,)
    )

    book_id = cursor.fetchone()[0]

    cursor.execute(
        '''
        DELETE FROM borrow_books
        WHERE id=%s
        ''',
        (id,)
    )

    cursor.execute(
        '''
        UPDATE books
        SET available=available+1
        WHERE id=%s
        ''',
        (book_id,)
    )

    connection.commit()

    return redirect('/allocatedbooks')

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)