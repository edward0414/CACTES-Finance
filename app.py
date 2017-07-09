from flask import Flask, flash, redirect, render_template, request, g, session, url_for
from functools import wraps
import os
import sqlite3

app = Flask(__name__)

username = ""

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
        g.db = sqlite3.connect('CACTESFinance2017.db')
        g.db.row_factory = sqlite3.Row
        print "Connect to the database successfuly!"
        cur = g.db.execute('select * from Finance')
        rows = cur.fetchall()
        g.db.close()

    except sqlite3.OperationalError:
        flash("You have no database")

    username = "admin"
    return render_template('welcome.html', user=username, rows=rows)


@app.route('/addTranscation', methods=['GET', 'POST'])
def addTranscation():
    error = None
    if request.method == 'POST':
        try:
            date = request.form['date']
            staff = request.form['staff']
            event = request.form['event']
            income = request.form['income']
            expense = request.form['expense']

            g.db = sqlite3.connect('CACTESFinance2017.db')
            print "Connect to the database successfuly!"

            #auto update the balance
            cur = g.db.execute('SELECT Max(TranscationID), Balance FROM Finance')
            for row in cur.fetchall():
                balance = row[1]
            balance = int(balance) + int(income) - int(expense)
            
            cur = g.db.execute('INSERT INTO Finance (Date,Staff_Position,Event,Income,Expense,Balance) VALUES (?,?,?,?,?,?)',(date,staff,event,income,expense,balance))
            g.db.commit()
            g.db.close()
            error = "Record successfully added!"
            return redirect(url_for('welcome'))

        except sqlite3.OperationalError:
            error = "Fail to insert new data"
            print "Failed"


    return render_template('addTranscation.html', error=error)



@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        print "login post received"

        if request.form['password'] == 'password' and request.form['username'] == 'admin':
            session['logged_in'] = True
            return redirect(url_for('welcome'))
        else:
            error = 'Invalid credentials. Please try again.'
    return render_template('login.html', error=error)



@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have just logged out')
    return redirect(url_for('home'))



@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')




@app.route('/signup', methods=['POST'])
def signup():
    fname = request.form['inputfName']
    lname = request.form['inputlName']
    email = request.form['inputEmail']
    password = request.form['inputPassword']



if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
