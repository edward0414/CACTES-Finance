from flask import Flask, flash, redirect, render_template, request, g, session, url_for
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import os
import sqlite3

# create the application object
app = Flask(__name__)

# config
app.config.from_object('config.DevelopmentConfig')

# create the sqlalchemy object
db = SQLAlchemy(app)

from models import *

user = ''


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
    # try:
    #     g.db = sqlite3.connect('CACTES.db')
    #     g.db.row_factory = sqlite3.Row
    #     #Select from Van
    #     cur = g.db.execute('select * from Vancouver')
    #     van = cur.fetchall()

    #     #Select from Surrey
    #     cur = g.db.execute('select * from Surrey')
    #     surrey = cur.fetchall()

    #     #Select from Delta
    #     cur = g.db.execute('select * from Delta')
    #     delta = cur.fetchall()

    #     #Select from Coquitlam
    #     cur = g.db.execute('select * from Coquitlam')
    #     coquitlam = cur.fetchall()

    #     #Select from Total
    #     cur = g.db.execute('select * from Total')
    #     total = cur.fetchall()

    #     g.db.close()

    # except sqlite3.OperationalError:
    #     flash("You have no database")

    
    van = db.session.query(Vancouver).all()
    surrey = db.session.query(Surrey).all()
    delta = db.session.query(Delta).all()
    coquitlam = db.session.query(Coquitlam).all()
    total = db.session.query(Total).all()

    return render_template('welcome.html', user=user, vans=van, surreys=surrey, deltas=delta, coquitlams=coquitlam, totals=total)


@app.route('/addTransaction', methods=['GET', 'POST'])
def addTransaction():
    error = None
    if request.method == 'POST':
        try:
            district = request.form['district']
            date = request.form['date']
            staff = request.form['staff']
            event = request.form['event']
            income = request.form['income']
            expense = request.form['expense']

            g.db = sqlite3.connect('CACTES.db')

            diff = int(income) - int(expense)

            #auto update the balance
            cur = g.db.execute("SELECT Max(TransactionID), Balance FROM {}".format(district))
            for row in cur.fetchall():
                transID = row[0]
                balance = row[1]
            transID = int(transID) + 1
            balance = int(balance) + diff
            
            cur = g.db.execute("INSERT INTO {} (Date,Person_Responsible,Event,Income,Expense,Balance) VALUES (?,?,?,?,?,?)".format(district),(date,staff,event,income,expense,balance))


            #auto update total
            cur = g.db.execute("SELECT Max(ID), Balance FROM Total")
            for row in cur.fetchall():
                balance = row[1]
            balance = int(balance) + diff

            cur = g.db.execute("INSERT INTO Total (District,ID_District,Date,Person_Responsible,Event,Income,Expense,Balance) VALUES (?,?,?,?,?,?,?,?)",(district,transID,date,staff,event,income,expense,balance))
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
        #Select from Van
        cur = g.db.execute('select * from Vancouver')
        van = cur.fetchall()

        #Select from Surrey
        cur = g.db.execute('select * from Surrey')
        surrey = cur.fetchall()

        #Select from Delta
        cur = g.db.execute('select * from Delta')
        delta = cur.fetchall()

        #Select from Coquitlam
        cur = g.db.execute('select * from Coquitlam')
        coquitlam = cur.fetchall()

        #Select from Total
        cur = g.db.execute('select * from Total')
        total = cur.fetchall()

        g.db.close()

    except sqlite3.OperationalError:
        error = "Fail to show the database"

    if request.method == 'POST':
        try:
            district = request.form['district']
            transID = request.form['transactionID']
            date = request.form['date']
            staff = request.form['staff']
            event = request.form['event']
            income = request.form['income']
            expense = request.form['expense']

            print(1)

            g.db = sqlite3.connect('CACTES.db')

            #auto update the balance
            cur = g.db.execute('SELECT Balance FROM {} WHERE TransactionID={}'.format(district, int(transID)-1))
            for row in cur.fetchall():
                balance = row[0]
            balance = int(balance) + int(income) - int(expense)
            print(2)
            
            #calculate the difference between the updated balance and the original balance
            cur = g.db.execute('SELECT Balance FROM {} WHERE TransactionID={}'.format(district, transID))
            for row in cur.fetchall():
                temp = row[0]
            diff = int(temp) - balance
            print(3)

            #Update this transaction in the district and Total
            print(district)
            cur = g.db.execute("UPDATE {} SET Date='{}',Person_Responsible='{}',Event='{}',Income={},Expense={},Balance={} WHERE TransactionID={}".format(district,date,staff,event,income,expense,balance,transID))
            print("a")
            cur = g.db.execute("UPDATE Total SET Date='{}',Person_Responsible='{}',Event='{}',Income={},Expense={} WHERE District='{}' AND ID_District={}".format(date,staff,event,income,expense,district,transID))
            print(4)

            #Update the balance of other transactions in the district
            cur = g.db.execute("UPDATE {} SET Balance=Balance-{} WHERE TransactionID>{}".format(district,diff,transID))
            print(5)

            #Update the balance of other trans in Total
            cur = g.db.execute("SELECT ID FROM Total WHERE District='{}' AND ID_District={}".format(district, transID))
            for row in cur.fetchall():
                ID = row[0]
            cur = g.db.execute("UPDATE Total SET Balance=Balance-{} WHERE ID>={}".format(diff,ID))
            print(6)

            g.db.commit()
            g.db.close()
            error = "Record successfully added!"
            return redirect(url_for('welcome'))

        except sqlite3.OperationalError:
            error = "Fail to modify data"


    return render_template('modifyTransaction.html', error=error, vans=van, surreys=surrey, deltas=delta, coquitlams=coquitlam, totals=total)



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
        credential = db.session.query(Staff).filter_by(email=request.form['email']).first()
        if (credential is None):
            error = 'Invalid credentials. Please try again.'

        else:
            if credential.password != request.form['password']:
                error = 'Invalid credentials. Please try again.'
            else:
                global user
                user = credential.fName
                session['logged_in'] = True
                return redirect(url_for('welcome'))


    return render_template('login.html', error=error)




@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have just logged out')
    return redirect(url_for('home'))




if __name__ == "__main__":
    app.run(host='0.0.0.0',port=4000)
