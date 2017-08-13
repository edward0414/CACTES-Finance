from flask import Flask, flash, redirect, render_template, request, g, session, url_for
from functools import wraps
import os
import sqlite3

app = Flask(__name__)
app.secret_key = 'CACTES'

user = ""

#login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to log in first.')
            return redirect(url_for('login'))
    return wrap



@app.route('/')
def home():
    return render_template('index.html')



@app.route('/welcome')
@login_required
def welcome():
    try:
        g.db = sqlite3.connect('CACTES.db')
        g.db.row_factory = sqlite3.Row
        cur = g.db.execute('select * from Finance')
        rows = cur.fetchall()
        g.db.close()

    except sqlite3.OperationalError:
        flash("You have no database")

    return render_template('welcome.html', user=user, rows=rows)


@app.route('/addTransaction', methods=['GET', 'POST'])
def addTransaction():
    error = None
    if request.method == 'POST':
        try:
            date = request.form['date']
            staff = request.form['staff']
            event = request.form['event']
            income = request.form['income']
            expense = request.form['expense']

            g.db = sqlite3.connect('CACTES.db')

            #auto update the balance
            cur = g.db.execute('SELECT Max(TransactionID), Balance FROM Finance')
            for row in cur.fetchall():
                balance = row[1]
            balance = int(balance) + int(income) - int(expense)
            
            cur = g.db.execute('INSERT INTO Finance (Date,Person_Responsible,Event,Income,Expense,Balance) VALUES (?,?,?,?,?,?)',(date,staff,event,income,expense,balance))
            g.db.commit()
            g.db.close()
            error = "Record successfully added!"
            return redirect(url_for('welcome'))

        except sqlite3.OperationalError:
            error = "Fail to insert new data"


    return render_template('addTransaction.html', error=error)


@app.route('/modifyTransaction', methods=['GET', 'POST'])
def modifyTransaction():
    error = None
    try:
        g.db = sqlite3.connect('CACTES.db')
        g.db.row_factory = sqlite3.Row
        cur = g.db.execute('SELECT * FROM Finance')
        rows = cur.fetchall()
        g.db.close()

    except sqlite3.OperationalError:
        error = "Fail to show the database"

    if request.method == 'POST':
        try:
            transactionID = request.form['transactionID']
            date = request.form['date']
            staff = request.form['staff']
            event = request.form['event']
            income = request.form['income']
            expense = request.form['expense']

            g.db = sqlite3.connect('CACTES.db')

            #auto update the balance
            cur = g.db.execute('SELECT Balance FROM Finance WHERE TransactionID=?', (int(transactionID)-1,))
            for row in cur.fetchall():
                balance = row[0]
            balance = int(balance) + int(income) - int(expense)
            
            #calculate the difference between the updated balance and the original balance
            cur = g.db.execute('SELECT Balance FROM Finance WHERE TransactionID=?', (transactionID,))
            for row in cur.fetchall():
                temp = row[0]
            diff = int(temp) - balance

            #Update this transaction
            cur = g.db.execute('UPDATE Finance SET Date=?,Person_Responsible=?,Event=?,Income=?,Expense=?,Balance=? WHERE TransactionID=?',(date,staff,event,income,expense,balance,transactionID))

            #Update the balance of every other transactions
            cur = g.db.execute('UPDATE Finance SET Balance=Balance-? WHERE TransactionID>?', (diff,transactionID))
            

            g.db.commit()
            g.db.close()
            error = "Record successfully added!"
            return redirect(url_for('welcome'))

        except sqlite3.OperationalError:
            error = "Fail to modify data"


    return render_template('modifyTransaction.html', error=error, rows=rows)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
#Hash the password!!

    error = None
    if request.method == 'POST':
        try:
            fname = request.form['fname']
            lname = request.form['lname']
            username = request.form['username']
            password = request.form['password']
            school = request.form['school']
            email = request.form['email']
            position = request.form['position']

            g.db = sqlite3.connect('CACTES.db')
            
            cur = g.db.execute('INSERT INTO Staff (FirstName,LastName,Username,Password,School,Email,Position) VALUES (?,?,?,?,?,?,?)',(fname,lname,username,password,school,email,position))
            g.db.commit()
            g.db.close()
            error = "Sign up successfully!"
            return redirect(url_for('login'))

        except sqlite3.OperationalError:
            error = "Fail to sign up."

    return render_template('signup.html', error=error)



@app.route('/login', methods=['GET','POST'])
def login():
#Hash the password!!

    error = None
    if request.method == 'POST':
        try:
            username = request.form['username']
            global user 
            user = username

            g.db = sqlite3.connect('CACTES.db')
            cur = g.db.execute("SELECT Password FROM Staff WHERE Username='{}'".format(username))
            for row in cur.fetchall():
                password = row[0]
            
            g.db.close()

            if request.form['password'] == password:
                session['logged_in'] = True
                return redirect(url_for('welcome'))
            else:
                error = 'Invalid credentials. Please try again.'

        except sqlite3.OperationalError:
            error = "Fail to log in."

    return render_template('login.html', error=error)




@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have just logged out')
    return redirect(url_for('home'))




if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=4000)
