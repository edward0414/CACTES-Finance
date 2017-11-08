from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Staff(db.Model):

	staff_id = db.Column(db.Integer, primary_key=True)
	f_name = db.Column(db.String(20), nullable=False)
	l_name = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(60), nullable=False)
	password = db.Column(db.String(120), nullable=False)
	rank = db.Column(db.String(25), nullable=False)
	district = db.Column(db.String(25), nullable=False) 
	position = db.Column(db.String(25), nullable=False)
	school = db.Column(db.String(25), nullable=False)
	seen = db.Column(db.Integer, nullable=False)

	def __init__(self, fName, lName, email, password, rank, district, position, school):
		self.f_name = fName
		self.l_name = lName
		self.email = email
		self.password = generate_password_hash(password)
		self.rank = rank
		self.district = district
		self.position = position
		self.school = school
		self.seen = 0

	def __repr__(self):
		return "<{} {}, position:{}>".format(self.f_name, self.l_name, self.position)

	def check_password(self, password):
		return check_password_hash(self.password, password)


class Cheque(db.Model):
	cheque_id = db.Column(db.Integer, primary_key=True)
	cheque_type = db.Column(db.String(15), nullable=False)
	cheque_num = db.Column(db.String(20), nullable=False)
	issued_by = db.Column(db.String(50), nullable=False)
	pay_to = db.Column(db.String(50), nullable=False)
	amount = db.Column(db.Integer, nullable=False)
	transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.transaction_id'), nullable=True)

	def __init__(self, chequeType, chequeNum, issuedBy, payTo, amount, transactionID):
		self.cheque_type = chequeType
		self.cheque_num = chequeNum
		self.issued_by = issuedBy
		self.pay_to = payTo
		self.amount = amount
		self.transaction_id = transactionID

	def __repr__(self):
		return "<Cheque {}: ${}, by {}>".format(self.cheque_num, self.amount, self.issued_by)


class MoneyCount(db.Model):
	money_count_id = db.Column(db.Integer, primary_key=True)
	money_type = db.Column(db.String(15), nullable=False)
	nickel = db.Column(db.Integer, nullable=False)
	dime = db.Column(db.Integer, nullable=False)
	quarter = db.Column(db.Integer, nullable=False)
	loonie = db.Column(db.Integer, nullable=False)
	toonie = db.Column(db.Integer, nullable=False)
	bill5 = db.Column(db.Integer, nullable=False)
	bill10 = db.Column(db.Integer, nullable=False)
	bill20 = db.Column(db.Integer, nullable=False)
	bill50 = db.Column(db.Integer, nullable=False)
	bill100 = db.Column(db.Integer, nullable=False)
	total = db.Column(db.Integer, nullable=False)
	transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.transaction_id'), nullable=False)

	def __init__(self, moneyType, numNickel, numDime, numQuarter, numLoonie, numToonie, num5bill, num10bill, num20bill, num50bill, num100bill, total, transactionID):
		self.money_type = moneyType
		self.nickel = numNickel
		self.dime = numDime
		self.quarter = numQuarter
		self.loonie = numLoonie
		self.toonie = numToonie
		self.bill5 = num5bill
		self.bill10 = num10bill
		self.bill20 = num20bill
		self.bill50 = num50bill
		self.bill100 = num100bill
		self.total = total
		self.transaction_id = transactionID

	def __repr__(self):
		return "<5 cents:{}, 10 cents:{}, 25 cents:{}, $1:{}, $2:{}, $5:{}, $10:{}, $20:{}, $50:{}, $100:{}>".format(self.nickel, self.dime, self.quarter, self.loonie, self.toonie, self.bill5, self.bill10, self.bill20, self.bill50, self.bill100)


class Transaction(db.Model):
	transaction_id = db.Column(db.Integer, primary_key=True)
	trans_type = db.Column(db.String(20), nullable=False)
	date = db.Column(db.Text, nullable=False)
	person_responsible = db.Column(db.String(25), nullable=False)
	approved_by = db.Column(db.String(25), nullable=False)
	event = db.Column(db.String(25), nullable=False)
	income = db.Column(db.Integer, nullable=False)
	expense = db.Column(db.Integer, nullable=False)
	last_edit = db.Column(db.String(40), nullable=False)
	last_edit_time = db.Column(db.Text, nullable=False)
	money_count_id = db.relationship('MoneyCount', backref='Transaction', lazy=True)
	cheque_id = db.relationship('Cheque', backref='Transaction', lazy=True)
	

	def __init__(self, transType, date, person, approvedBy, event, income, expense, lastEdit, lastEditTime):
		self.trans_type = transType
		self.date = date
		self.person_responsible = person
		self.approved_by = approvedBy
		self.event = event
		self.income = income
		self.expense = expense
		self.last_edit = lastEdit
		self.last_edit_time = lastEditTime

	def __repr__(self):
		return "<{}: {}, {}, net:{}>".format(self.type, self.event, self.date, (self.income-self.expense))


