from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify, make_response
from datetime import datetime
from pytz import timezone
import pytz
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc
import os

# create the application object
app = Flask(__name__)

# config
app.config.from_object(os.environ['APP_SETTINGS'])

# create the sqlalchemy object
db = SQLAlchemy(app)

from models import *


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
    
    authorized = session['authorized']
    district = session['district']

    if authorized is True:
        transactions = db.session.query(Transaction).all()
        session['notSeen'] = len(transactions) - session['seen']
    else:
        transactions = db.session.query(Transaction).filter_by(transType=(district)).all()
        session['notSeen'] = len(transactions) - session['seen']

    db.session.close()

    return render_template('welcome.html', user=session['user'], transactions=transactions, 
        authorized=authorized, district=district, notSeen=session['notSeen'])


@app.route('/addTransaction', methods=['GET', 'POST'])
@login_required
def addTransaction():

    error = None
    if request.method == 'POST':
        try:
            transType = request.form['type']
            date = request.form['date']
            staff = request.form['staff']
            approved = request.form['approved']
            event = request.form['event']
            income = int(request.form['income'])
            expense = int(request.form['expense'])


            e_Count = {}
            #store info for the numbers of coins and bills spent (expense)
            i_Count = {}
            #store info for the numbers of coins and bills earned (income)


            e_Count["Nickel"] = int(request.form['e-numNickel'])
            e_Count["Dime"] = int(request.form['e-numDime'])
            e_Count["Quarter"] = int(request.form['e-numQuarter'])
            e_Count["Loonie"] = int(request.form['e-numLoonie'])
            e_Count["Toonie"] = int(request.form['e-numToonie'])
            e_Count["5bill"] = int(request.form['e-num5bill'])
            e_Count["10bill"] = int(request.form['e-num10bill'])
            e_Count["20bill"] = int(request.form['e-num20bill'])
            e_Count["50bill"] = int(request.form['e-num50bill'])
            e_Count["100bill"] = int(request.form['e-num100bill'])

            i_Count["Nickel"] = int(request.form['i-numNickel'])
            i_Count["Dime"] = int(request.form['i-numDime'])
            i_Count["Quarter"] = int(request.form['i-numQuarter'])
            i_Count["Loonie"] = int(request.form['i-numLoonie'])
            i_Count["Toonie"] = int(request.form['i-numToonie'])
            i_Count["5bill"] = int(request.form['i-num5bill'])
            i_Count["10bill"] = int(request.form['i-num10bill'])
            i_Count["20bill"] = int(request.form['i-num20bill'])
            i_Count["50bill"] = int(request.form['i-num50bill'])
            i_Count["100bill"] = int(request.form['i-num100bill'])


            exist = db.session.query(Transaction).order_by(desc(Transaction.transaction_id)).limit(1).scalar() is not None

            if not exist:
                transactionID = 1
            else:
                cur = db.session.query(Transaction).order_by(desc(Transaction.transaction_id)).limit(1)
                transactionID = int(cur[0].transaction_id) + 1


            etotal = e_Count['Nickel']*0.05 + e_Count['Dime']*0.1 + e_Count['Quarter']*0.25 + \
            e_Count['Loonie'] + e_Count['Toonie']*2 + e_Count['5bill']*5 + e_Count['10bill']*10 + \
            e_Count['20bill']*20 + e_Count['50bill']*50 + e_Count['100bill']*100

            itotal = i_Count['Nickel']*0.05 + i_Count['Dime']*0.1 + i_Count['Quarter']*0.25 + \
            i_Count['Loonie'] + i_Count['Toonie']*2 + i_Count['5bill']*5 + i_Count['10bill']*10 + \
            i_Count['20bill']*20 + i_Count['50bill']*50 + i_Count['100bill']*100



            numCheques = int(request.form['numCheq'])
            chequeType = request.form.getlist('chequeType')
            chequeNum = request.form.getlist('chequeNum')
            issuedBy = request.form.getlist('issuedBy')
            payTo = request.form.getlist('payTo')
            chequeAmount = request.form.getlist('chequeAmount')


            if numCheques == 0:
                if etotal != expense or itotal != income:
                    error= "Expense or income total does not match with the sum of the coin(s)." + \
                    " Please check if you enter the right number."
                    raise Exception(error)

            else:
                eSum = etotal
                iSum = itotal
                for i in range(numCheques):
                    if chequeType[i] == "Income":
                        iSum += int(chequeAmount[i])
                    elif chequeType[i] == "Expense":
                        eSum += int(chequeAmount[i]) 

                if eSum != expense or iSum != income:
                    error= "Expense or income total does not match with the sum of coins and cheque(s)." + \
                    " Please check if you enter the right number."
                    raise Exception(error)


            for i in range(numCheques):
                db.session.add(Cheque(chequeType[i], chequeNum[i], issuedBy[i], payTo[i], chequeAmount[i], transactionID))


            time_format='%Y-%m-%d %H:%M:%S %Z'
            time = datetime.now(tz=pytz.utc)
            time = time.astimezone(timezone('Canada/Pacific'))

            db.session.add(Transaction(transType, date, staff, approved, event, income, expense, session['user'], 
                time.strftime(time_format) ))


            db.session.add(MoneyCount("Income", i_Count['Nickel'], i_Count['Dime'], i_Count['Quarter'], 
                i_Count['Loonie'], i_Count['Toonie'], i_Count['5bill'], i_Count['10bill'], i_Count['20bill'], 
                i_Count['50bill'], i_Count['100bill'], itotal, transactionID))

            db.session.add(MoneyCount("Expense", e_Count['Nickel'], e_Count['Dime'], e_Count['Quarter'], 
                e_Count['Loonie'], e_Count['Toonie'], e_Count['5bill'], e_Count['10bill'], e_Count['20bill'], 
                e_Count['50bill'], e_Count['100bill'], etotal, transactionID))

            db.session.commit()
            db.session.close()
            error = "Record successfully added!"
            return redirect(url_for('welcome'))


        except Exception as e:
            print('fail adding')
            error= "Fail to add transaction. " + str(e.args[0])

    return render_template('addTransaction.html', error=error, authorized=session['authorized'] ,district=session['district'])



@app.route('/modifyTransaction/<transactionID>', methods=['GET', 'POST'])
@login_required
def modifyTransaction(transactionID):

    error = None

    transaction = db.session.query(Transaction).filter_by(transaction_id=(transactionID)).first()
    money = db.session.query(MoneyCount).filter_by(transaction_id=(transactionID)).all() #list
    for item in money:
        if item.money_type == "Income":
            i_money = item
        elif item.money_type == "Expense":
            e_money = item


    if request.method == 'POST':
        try:
            transID = transactionID
            transType = request.form['type']
            date = request.form['date']
            staff = request.form['staff']
            approved = request.form['approved']
            event = request.form['event']
            income = int(request.form['income'])
            expense = int(request.form['expense'])

            result = db.session.query(Transaction).filter_by(transaction_id=transID).first()

            if result is None:
                error = "Invalid transaction ID. Please make sure you have the right transaction ID."
                raise Exception(error)

            time_format='%Y-%m-%d %H:%M:%S %Z'
            time = datetime.now(tz=pytz.utc)
            time = time.astimezone(timezone('Canada/Pacific'))

            db.session.query(Transaction).filter_by(transaction_id=transID).update({"trans_type":transType, 
                "date":date, "person_responsible":staff, "approved_by":approved, "event":event, "income":income, "expense":expense, 
                "last_edit":session['user'], "last_edit_time":time.strftime(time_format)})

            e_Count = {}
            #store info for the numbers of coins and bills spent (expense)
            i_Count = {}
            #store info for the numbers of coins and bills earned (income)


            e_Count["Nickel"] = int(request.form['e-numNickel'])
            e_Count["Dime"] = int(request.form['e-numDime'])
            e_Count["Quarter"] = int(request.form['e-numQuarter'])
            e_Count["Loonie"] = int(request.form['e-numLoonie'])
            e_Count["Toonie"] = int(request.form['e-numToonie'])
            e_Count["5bill"] = int(request.form['e-num5bill'])
            e_Count["10bill"] = int(request.form['e-num10bill'])
            e_Count["20bill"] = int(request.form['e-num20bill'])
            e_Count["50bill"] = int(request.form['e-num50bill'])
            e_Count["100bill"] = int(request.form['e-num100bill'])

            i_Count["Nickel"] = int(request.form['i-numNickel'])
            i_Count["Dime"] = int(request.form['i-numDime'])
            i_Count["Quarter"] = int(request.form['i-numQuarter'])
            i_Count["Loonie"] = int(request.form['i-numLoonie'])
            i_Count["Toonie"] = int(request.form['i-numToonie'])
            i_Count["5bill"] = int(request.form['i-num5bill'])
            i_Count["10bill"] = int(request.form['i-num10bill'])
            i_Count["20bill"] = int(request.form['i-num20bill'])
            i_Count["50bill"] = int(request.form['i-num50bill'])
            i_Count["100bill"] = int(request.form['i-num100bill'])


            etotal = e_Count['Nickel']*0.05 + e_Count['Dime']*0.1 + e_Count['Quarter']*0.25 + \
            e_Count['Loonie'] + e_Count['Toonie']*2 + e_Count['5bill']*5 + e_Count['10bill']*10 + \
            e_Count['20bill']*20 + e_Count['50bill']*50 + e_Count['100bill']*100

            itotal = i_Count['Nickel']*0.05 + i_Count['Dime']*0.1 + i_Count['Quarter']*0.25 + \
            i_Count['Loonie'] + i_Count['Toonie']*2 + i_Count['5bill']*5 + i_Count['10bill']*10 + \
            i_Count['20bill']*20 + i_Count['50bill']*50 + i_Count['100bill']*100





            moneyCounts = db.session.query(MoneyCount).filter_by(transaction_id=transID).all()
            for item in moneyCounts:
                if item.money_type == "Income":
                    item.nickel = i_Count['Nickel']
                    item.dime = i_Count['Dime']
                    item.quarter = i_Count['Quarter']
                    item.loonie = i_Count['Loonie']
                    item.toonie = i_Count['Toonie']
                    item.bill5 = i_Count['5bill']
                    item.bill10 = i_Count['10bill']
                    item.bill20 = i_Count['20bill']
                    item.bill50 = i_Count['50bill']
                    item.bill100 = i_Count['100bill']
                    item.total = itotal

                elif item.money_type == "Expense":
                    item.nickel = e_Count['Nickel']
                    item.dime = e_Count['Dime']
                    item.quarter = e_Count['Quarter']
                    item.loonie = e_Count['Loonie']
                    item.toonie = e_Count['Toonie']
                    item.bill5 = e_Count['5bill']
                    item.bill10 = e_Count['10bill']
                    item.bill20 = e_Count['20bill']
                    item.bill50 = e_Count['50bill']
                    item.bill100 = e_Count['100bill']
                    item.total = etotal

      

            numCheques = int(request.form['numCheq'])
            chequeType = request.form.getlist('chequeType')
            chequeNum = request.form.getlist('chequeNum')
            issuedBy = request.form.getlist('issuedBy')
            payTo = request.form.getlist('payTo')
            chequeAmount = request.form.getlist('chequeAmount')


            if numCheques == 0:
                if etotal != expense or itotal != income:
                    error= "Expense or income total does not match with the sum of the coin(s)."+ \
                    " Please check if you enter the right number."

                    raise Exception(error)
            else:
                eSum = etotal
                iSum = itotal
                for i in range(numCheques):
                    if chequeType[i] == "Income":
                        iSum += int(chequeAmount[i])
                    elif chequeType[i] == "Expense":
                        eSum += int(chequeAmount[i]) 

                if eSum != expense or iSum != income:
                    error= "Expense or income total does not match with the sum of coins and cheque(s)."+ \
                    " Please check if you enter the right number."

                    raise Exception(error)


            cheques = db.session.query(Cheque).filter_by(transaction_id=transID).all()

            if len(cheques) == numCheques:
                for i in range(numCheques):
                    cheques[i].cheque_type = chequeType[i]
                    cheques[i].cheque_num = chequeNum[i]
                    cheques[i].issued_by = issuedBy[i]
                    cheques[i].pay_to = payTo[i]
                    cheques[i].amount = chequeAmount[i]
            

            elif len(cheques) < numCheques:
                for i in range(len(cheques)):
                    cheques[i].cheque_type = chequeType[i]
                    cheques[i].cheque_num = chequeNum[i]
                    cheques[i].issued_by = issuedBy[i]
                    cheques[i].pay_to = payTo[i]
                    cheques[i].amount = chequeAmount[i]

                for i in range(numCheques - len(cheques)):
                    db.session.add(Cheque(chequeType[i+len(cheques)], chequeNum[i+len(cheques)], 
                        issuedBy[i+len(cheques)], payTo[i+len(cheques)], chequeAmount[i+len(cheques)], transID))


            elif len(cheques) > numCheques:
                for i in range(numCheques):
                    cheques[i].cheque_type = chequeType[i]
                    cheques[i].cheque_num = chequeNum[i]
                    cheques[i].issued_by = issuedBy[i]
                    cheques[i].pay_to = payTo[i]
                    cheques[i].amount = chequeAmount[i]

                for i in range(len(cheques) - numCheques):
                    db.session.delete(cheques[i + numCheques])




            db.session.commit()
            db.session.close()
            error = "Record successfully added!"
            return redirect(url_for('welcome'))

        except Exception as e:
            print('fail modifying')
            error= "Fail to modify transaction. " + str(e.args[0])


    return render_template('modifyTransaction.html', error=error, transaction=transaction, 
        i_money=i_money, e_money=e_money, authorized=session['authorized'] ,district=session['district'])




@app.route('/transactions/<transactionID>')
@login_required
def transactions(transactionID):

    transaction = db.session.query(Transaction).filter_by(transaction_id=(transactionID)).first()
    money = db.session.query(MoneyCount).filter_by(transaction_id=(transactionID)).all() #list
    cheques = db.session.query(Cheque).filter_by(transaction_id=(transactionID)).all() #list


    transactionInfo = {'transType': transaction.trans_type,
                        'date': transaction.date,
                        'person': transaction.person_responsible,
                        'approvedBy': transaction.approved_by,
                        'event': transaction.event,
                        'income': transaction.income,
                        'expense': transaction.expense,
                        'lastEdit': transaction.last_edit,
                        'lastEditTime': transaction.last_edit_time}

    moneyCount = []
    if len(money) != 0:
        moneyCount.append({"moneyType":money[0].money_type,
                                "numNickel":money[0].nickel,
                                "numDime":money[0].dime,
                                "numQuarter":money[0].quarter,
                                "numLoonie":money[0].loonie,
                                "numToonie":money[0].toonie,
                                "num5bill":money[0].bill5,
                                "num10bill":money[0].bill10,
                                "num20bill":money[0].bill20,
                                "num50bill":money[0].bill50,
                                "num100bill":money[0].bill100,
                                "total":money[0].total})

        moneyCount.append({"moneyType":money[1].money_type,
                                "numNickel":money[1].nickel,
                                "numDime":money[1].dime,
                                "numQuarter":money[1].quarter,
                                "numLoonie":money[1].loonie,
                                "numToonie":money[1].toonie,
                                "num5bill":money[1].bill5,
                                "num10bill":money[1].bill10,
                                "num20bill":money[1].bill20,
                                "num50bill":money[1].bill50,
                                "num100bill":money[1].bill100,
                                "total":money[1].total})


    cheque = []
    if len(cheques) != 0:
        for i in range(len(cheques)):
            cheque.append({"chequeType":cheques[i].cheque_type,
                                "chequeNum":cheques[i].cheque_num,
                                "issuedBy":cheques[i].issued_by,
                                "payTo":cheques[i].pay_to,
                                "amount":cheques[i].amount})


    db.session.close()
    return jsonify({"transaction": transactionInfo, "moneyCounts":moneyCount, "cheques":cheque})




@app.route('/signup', methods=['GET', 'POST'])
def signup():
#Hash the password!!

    error = None
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        rank = request.form['rank']
        district = request.form['district']
        position = request.form['position']
        school = request.form['school']

        db.session.add(Staff(fname, lname, email, password, rank, district, position, school))
        db.session.commit()
        db.session.close()
        error = "Sign up successfully!"
        return redirect(url_for('login'))

    return render_template('signup.html', error=error)



@app.route('/login', methods=['GET','POST'])
def login():
#Unhash the password!!

    error = None
    if request.method == 'POST':
        credential = db.session.query(Staff).filter_by(email=request.form['email']).first()
        if (credential is None):
            error = 'Not a registered email. Please sign up!'

        else:
            if not credential.check_password(request.form['password']):
                error = 'Invalid credentials. Please try again.'
            else:
                session['user'] = credential.f_name + " " + credential.l_name
                session['email'] = credential.email
                session['seen'] = credential.seen
                session['notSeen'] = 0
                session['logged_in'] = True
                session['authorized'] = (credential.rank != 'Junior')
                session['district'] = credential.district
                return redirect(url_for('welcome'))


    db.session.close()
    return render_template('login.html', error=error)




@app.route('/logout')
def logout():
    user = db.session.query(Staff).filter_by(email=session['email']).first()
    user.seen = session['notSeen'] + session['seen']
    db.session.commit()
    db.session.close()

    session.pop('user', None)
    session.pop('logged_in', None)
    session.pop('authorized', None)
    session.pop('district', None)
    session.pop('seen', None)
    session.pop('notSeen', None)
    session.pop('email', None)
    flash('You have just logged out')
    return redirect(url_for('home'))




if __name__ == "__main__":
    app.run(host='0.0.0.0',port=4000)
