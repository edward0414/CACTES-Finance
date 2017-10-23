from app import db, bcrypt


class Staff(db.Model):

	staffID = db.Column(db.Integer, primary_key=True)
	fName = db.Column(db.String(12), nullable=False)
	lName = db.Column(db.String(12), nullable=False)
	email = db.Column(db.String(60), nullable=False)
	password = db.Column(db.String(30), nullable=False)
	rank = db.Column(db.String(25), nullable=False)
	district = db.Column(db.String(25), nullable=False) 
	position = db.Column(db.String(25), nullable=False)
	school = db.Column(db.String(25), nullable=False)
	seen = db.Column(db.Integer, nullable=False)

	def __init__(self, fName, lName, email, password, rank, district, position, school):
		self.fName = fName
		self.lName = lName
		self.email = email
		self.password = bcrypt.generate_password_hash(password)
		self.rank = rank
		self.district = district
		self.position = position
		self.school = school
		self.seen = 0

	def __repr__(self):
		return "<{} {}, position:{}>".format(self.fName, self.lName, self.position)


class Cheque(db.Model):
	chequeID = db.Column(db.Integer, primary_key=True)
	chequeType = db.Column(db.String(15), nullable=False)
	chequeNum = db.Column(db.String(20), nullable=False)
	issuedBy = db.Column(db.String(50), nullable=False)
	payTo = db.Column(db.String(50), nullable=False)
	amount = db.Column(db.Integer, nullable=False)
	transactionID = db.Column(db.Integer, db.ForeignKey('transaction.transactionID'), nullable=True)

	def __init__(self, chequeType, chequeNum, issuedBy, payTo, amount, transactionID):
		self.chequeType = chequeType
		self.chequeNum = chequeNum
		self.issuedBy = issuedBy
		self.payTo = payTo
		self.amount = amount
		self.transactionID = transactionID

	def __repr__(self):
		return "<Cheque {}: ${}, by {}>".format(self.chequeNum, self.amount, self.issuedBy)


class MoneyCount(db.Model):
	moneyCountID = db.Column(db.Integer, primary_key=True)
	moneyType = db.Column(db.String(15), nullable=False)
	numNickel = db.Column(db.Integer, nullable=False)
	numDime = db.Column(db.Integer, nullable=False)
	numQuarter = db.Column(db.Integer, nullable=False)
	numLoonie = db.Column(db.Integer, nullable=False)
	numToonie = db.Column(db.Integer, nullable=False)
	num5bill = db.Column(db.Integer, nullable=False)
	num10bill = db.Column(db.Integer, nullable=False)
	num20bill = db.Column(db.Integer, nullable=False)
	num50bill = db.Column(db.Integer, nullable=False)
	num100bill = db.Column(db.Integer, nullable=False)
	total = db.Column(db.Integer, nullable=False)
	transactionID = db.Column(db.Integer, db.ForeignKey('transaction.transactionID'), nullable=False)

	def __init__(self, moneyType, numNickel, numDime, numQuarter, numLoonie, numToonie, num5bill, num10bill, num20bill, num50bill, num100bill, total, transactionID):
		self.moneyType = moneyType
		self.numNickel = numNickel
		self.numDime = numDime
		self.numQuarter = numQuarter
		self.numLoonie = numLoonie
		self.numToonie = numToonie
		self.num5bill = num5bill
		self.num10bill = num10bill
		self.num20bill = num20bill
		self.num50bill = num50bill
		self.num100bill = num100bill
		self.total = total
		self.transactionID = transactionID

	def __repr__(self):
		return "<5 cents:{}, 10 cents:{}, 25 cents:{}, $1:{}, $2:{}, $5:{}, $10:{}, $20:{}, $50:{}, $100:{}>".format(self.numNickel, self.numDime, self.numQuarter, self.numLoonie, self.numToonie, self.num5bill, self.num10bill, self.num20bill, self.num50bill, self.num100bill)


class Transaction(db.Model):
	transactionID = db.Column(db.Integer, primary_key=True)
	transType = db.Column(db.String(20), nullable=False)
	date = db.Column(db.text, nullable=False)
	personResponsible = db.Column(db.String(25), nullable=False)
	approvedBy = db.Column(db.String(25), nullable=False)
	event = db.Column(db.String(25), nullable=False)
	income = db.Column(db.Integer, nullable=False)
	expense = db.Column(db.Integer, nullable=False)
	moneyCountID = db.relationship('MoneyCount', backref='Transaction', lazy=True)
	cheque = db.relationship('Cheque', backref='Transaction', lazy=True)
	

	def __init__(self, transType, date, person, approvedBy, event, income, expense):
		self.transType = transType
		self.date = date
		self.personResponsible = person
		self.approvedBy = approvedBy
		self.event = event
		self.income = income
		self.expense = expense

	def __repr__(self):
		return "<{}: {}, {}, net:{}>".format(self.type, self.event, self.date, (self.income-self.expense))


