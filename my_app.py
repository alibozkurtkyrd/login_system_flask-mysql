from flask import Flask,render_template,request,url_for, session, redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = "your secret key"

# database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'logintest'
 
# intialize mysql
mysql = MySQL(app)

@app.route("/", methods=['GET', 'POST'])
def login():
    # inform message for user
    msg = ''
    # check if username and password POST request exist
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # create variable for store username and password information
        username = request.form['username']
        password = request.form['password']


        # let's look at account exists in our MySQL database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts where username = %s AND password=%s',(username,password,))
        account = cursor.fetchone()
          
        # if account exist in our accounts table 

        if account:

            # cursor 2 this is for our other_information table which contain authentication column

            cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor2.execute('select * from other_information where username= %s',(username,))
            authentication = cursor2.fetchone()

            session['loggedin'] = True # we use this data in other routes
            session['username'] = account['username']
            session['authentication'] = authentication['authentication']
            # route to home page
            return render_template('home.html',msg = username)

        else: # account no exist
            msg = 'Incorrect username/password!'
            
    return  render_template("login.html", msg=msg)

@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login.html'))    

@app.route('/auth', methods=['GET', 'POST'])
def authentication():
    # this function show the existing users' data to user who has admin authentication

    if ('loggedin' in session and session['authentication'] == 'Admin'):
    
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from accounts as a join other_information as o on a.username = o.username')
        accounts = cursor.fetchall()
        return render_template('auth.html', msg=accounts)
    return render_template('home.html', msg='you do NOT have  admin authentication')

@app.route('/upgrade', methods=['GET', 'POST'])
def upgrade():

    if ('loggedin' in session):


        if request.method == 'POST' and 'email' in request.form:

            email = request.form['email']

            cursor3 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor3.execute('UPDATE accounts SET email = %s WHERE username = %s',(email,session['username'],))
            mysql.connection.commit()
            return render_template('upgrade.html', msg = 'email updated')

    return render_template('upgrade.html', msg ='your email is not updated')
    
@app.route("/signup", methods=['GET', 'POST'])
def register():
    msg = '' # output message to inform user

    # check the user input 
    if request.method == 'POST' and 'username' in request.form and 'name' in request.form and 'surname' in request.form and 'email' in request.form and 'password' in request.form and 'address' in request.form and 'phone' in request.form and 'auth' in request.form:

        # variables
        username = request.form['username']
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email'] # previos one I mistakenly wrirte ...[password]
        address = request.form['address']
        phone = request.form['phone']
        auth = request.form['auth']
        password = request.form['password']
        
        
        # check accounts table from mysql
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor. execute('SELECT * FROM accounts WHERE username= %s',(username,)) 
        account = cursor.fetchone()

        # reduce the errors come from manually

        if account:
            msg = 'Account already exists!'   
        
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'

        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'name must contain only characters and numbers!'

        elif not re.match(r'[A-Za-z0-9]+', surname):
            msg = 'surname must contain only characters and numbers!'

        elif not re.match(r'[z0-9]+', phone):
            msg = 'phone  must contain only numbers!'

        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'

        elif not username or not name or not surname or not password or not email:
            msg = 'Please fill out the form!' 

        else:

            # Account doesnt exists and the form data is valid, now insert new account into accounts table

            cursor.execute('INSERT INTO accounts VALUES(%s, %s, %s)',(username,password,email,)) # for accounts table
            
            
            cursor.execute('INSERT INTO other_information VALUES(Null, %s, %s, %s, %s, %s, %s)',(username,name, surname,
                            phone,auth, address,)) # for accounts table
            mysql.connection.commit()
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        # Form is not satisfy required input
        msg = 'please fill out the form!'

    return  render_template("signup.html",msg = msg)
    
if __name__ == "__main__":
	app.run(debug =True)
