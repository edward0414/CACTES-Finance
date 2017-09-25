from flask import Flask, flash, redirect, render_template, request, session, url_for
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import os

# create the application object
app = Flask(__name__)

# config
app.config.from_object(os.environ['APP_SETTINGS'])
print(os.environ['APP_SETTINGS'])

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

        district = request.form['district']
        date = request.form['date']
        staff = request.form['staff']
        event = request.form['event']
        income = int(request.form['income'])
        expense = int(request.form['expense'])

        diff = income - expense

        #auto update the balance
        if district == "Vancouver":
            cur = db.session.query(Vancouver).order_by(desc(Vancouver.transactionID)).limit(1)
            transID = cur[0].transactionID
            balance = cur[0].balance

            transID = int(transID) + 1
            balance = int(balance) + diff
            db.session.add(Vancouver(date, staff, event, income, expense, balance))

        elif district == "Surrey":
            cur = db.session.query(Surrey).order_by(desc(Surrey.transactionID)).limit(1)
            transID = cur[0].transactionID
            balance = cur[0].balance

            transID = int(transID) + 1
            balance = int(balance) + diff
            db.session.add(Surrey(date, staff, event, income, expense, balance))

        elif district == "Coquitlam":
            cur = db.session.query(Coquitlam).order_by(desc(Coquitlam.transactionID)).limit(1)
            transID = cur[0].transactionID
            balance = cur[0].balance

            transID = int(transID) + 1
            balance = int(balance) + diff
            db.session.add(Coquitlam(date, staff, event, income, expense, balance))

        elif district == "Delta":
            cur = db.session.query(Delta).order_by(desc(Delta.transactionID)).limit(1)
            transID = cur[0].transactionID
            balance = cur[0].balance

            transID = int(transID) + 1
            balance = int(balance) + diff
            db.session.add(Delta(date, staff, event, income, expense, balance))


        #auto update total
        cur = db.session.query(Total).order_by(desc(Total.id)).limit(1)
        balance = cur[0].balance
        balance = int(balance) + diff

        db.session.add(Total(district, transID, date, staff, event, income, expense, balance))
        db.session.commit()
        error = "Record successfully added!"
        return redirect(url_for('welcome'))

    return render_template('addTransaction.html', error=error)



@app.route('/modifyTransaction', methods=['GET', 'POST'])
def modifyTransaction():
    error = None

    van = db.session.query(Vancouver).all()
    surrey = db.session.query(Surrey).all()
    delta = db.session.query(Delta).all()
    coquitlam = db.session.query(Coquitlam).all()
    total = db.session.query(Total).all()

    if request.method == 'POST':
        district = request.form['district']
        transID = request.form['transactionID']
        date = request.form['date']
        staff = request.form['staff']
        event = request.form['event']
        income = int(request.form['income'])
        expense = int(request.form['expense'])

        
        if district == "Vancouver":
            #auto update the balance
            cur = db.session.query(Vancouver).filter_by(transactionID=(int(transID)-1)).first()
            balance = cur.balance
            balance = int(balance) + income - expense

            #calculate the difference between the updated balance and the original balance
            cur = db.session.query(Vancouver).filter_by(transactionID=transID).first()
            temp = cur.balance
            diff = int(temp) - balance

            #Update this transaction in the district
            db.session.query(Vancouver).filter_by(transactionID=transID).update({"date":date, "personResponsible":staff, "event":event, "income":income, "expense":expense, "balance":balance})

            #Update the balance of other transactions in the district
            db.session.query(Vancouver).filter(Vancouver.transactionID > transID).update({"balance":(Vancouver.balance-diff)})


        elif district == "Coquitlam":
            #auto update the balance
            cur = db.session.query(Coquitlam).filter_by(transactionID=(int(transID)-1)).first()
            balance = cur.balance
            balance = int(balance) + income - expense

            #calculate the difference between the updated balance and the original balance
            cur = db.session.query(Coquitlam).filter_by(transactionID=transID).first()
            temp = cur.balance
            diff = int(temp) - balance

            #Update this transaction in the district
            db.session.query(Coquitlam).filter_by(transactionID=transID).update({"date":date, "personResponsible":staff, "event":event, "income":income, "expense":expense, "balance":balance})

            #Update the balance of other transactions in the district
            db.session.query(Coquitlam).filter(Coquitlam.transactionID > transID).update({"balance":(Coquitlam.balance-diff)})


        elif district == "Delta":
            #auto update the balance
            cur = db.session.query(Delta).filter_by(transactionID=(int(transID)-1)).first()
            balance = cur.balance
            balance = int(balance) + income - expense

            #calculate the difference between the updated balance and the original balance
            cur = db.session.query(Delta).filter_by(transactionID=transID).first()
            temp = cur.balance
            diff = int(temp) - balance

            #Update this transaction in the district
            db.session.query(Delta).filter_by(transactionID=transID).update({"date":date, "personResponsible":staff, "event":event, "income":income, "expense":expense, "balance":balance})

            #Update the balance of other transactions in the district
            db.session.query(Delta).filter(Delta.transactionID > transID).update({"balance":(Delta.balance-diff)})


        elif district == "Surrey":
            #auto update the balance
            cur = db.session.query(Surrey).filter_by(transactionID=(int(transID)-1)).first()
            balance = cur.balance
            balance = int(balance) + income - expense

            #calculate the difference between the updated balance and the original balance
            cur = db.session.query(Surrey).filter_by(transactionID=transID).first()
            temp = cur.balance
            diff = int(temp) - balance

            #Update this transaction in the district
            db.session.query(Surrey).filter_by(transactionID=transID).update({"date":date, "personResponsible":staff, "event":event, "income":income, "expense":expense, "balance":balance})

            #Update the balance of other transactions in the district
            db.session.query(Surrey).filter(Surrey.transactionID > transID).update({"balance":(Surrey.balance-diff)})


        #Update this trans and the balance of other trans in Total
        db.session.query(Total).filter_by(id_district=transID, district=district).update({"date":date, "personResponsible":staff, "event":event, "income":income, "expense":expense})
        cur = db.session.query(Total).filter_by(id_district=transID, district=district).first()
        id = int(cur.id) -1
        db.session.query(Total).filter(Total.id > id).update({"balance":(Total.balance-diff)})
        db.session.commit()
        error = "Record successfully added!"
        return redirect(url_for('welcome'))



    return render_template('modifyTransaction.html', error=error, vans=van, surreys=surrey, deltas=delta, coquitlams=coquitlam, totals=total)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
#Hash the password!!

    error = None
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        school = request.form['school']
        position = request.form['position']

        db.session.add(Staff(fname, lname, email, password, school, position))
        db.session.commit()
        error = "Sign up successfully!"
        return redirect(url_for('login'))

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
