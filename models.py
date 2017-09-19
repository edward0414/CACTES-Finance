from app import db


class Staff(db.Model):

	staffID = db.Column(db.Integer, primary_key=True)
	fName = db.Column(db.String(12), nullable=False)
	lName = db.Column(db.String(12), nullable=False)
	email = db.Column(db.String(60), nullable=False)
	password = db.Column(db.String(30), nullable=False)
	school = db.Column(db.String(25), nullable=False)
	position = db.Column(db.String(25), nullable=False)

	def __init__(self, fName, lName, email, password, school, position):
		self.fName = fName
		self.lName = lName
		self.email = email
		self.password = password
		self.school = school
		self.position = position

	def __repr__(self):
		return "<{} {}, position:{}>".format(self.fName, self.lName, self.position)


class Vancouver(db.Model):

	transactionID = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.Text, nullable=False)
	personResponsible = db.Column(db.String(25), nullable=False)
	event = db.Column(db.String(25), nullable=False)
	income = db.Column(db.Integer, nullable=False)
	expense = db.Column(db.Integer, nullable=False)
	balance = db.Column(db.Integer, nullable=False)

	def __init__(self, date, person, event, income, expense, balance):
		self.date = date
		self.personResponsible = person
		self.event = event
		self.income = income
		self.expense = expense
		self.balance = balance

	def __repr__(self):
		return "<{}, {}, net:{}>".format(self.event, self.date, (self.income-self.expense))


class Surrey(db.Model):

	transactionID = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.Text, nullable=False)
	personResponsible = db.Column(db.String(25), nullable=False)
	event = db.Column(db.String(25), nullable=False)
	income = db.Column(db.Integer, nullable=False)
	expense = db.Column(db.Integer, nullable=False)
	balance = db.Column(db.Integer, nullable=False)

	def __init__(self, date, person, event, income, expense, balance):
		self.date = date
		self.personResponsible = person
		self.event = event
		self.income = income
		self.expense = expense
		self.balance = balance

	def __repr__(self):
		return "<{}, {}, net:{}>".format(self.event, self.date, (self.income-self.expense))


class Delta(db.Model):

	transactionID = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.Text, nullable=False)
	personResponsible = db.Column(db.String(25), nullable=False)
	event = db.Column(db.String(25), nullable=False)
	income = db.Column(db.Integer, nullable=False)
	expense = db.Column(db.Integer, nullable=False)
	balance = db.Column(db.Integer, nullable=False)

	def __init__(self, date, person, event, income, expense, balance):
		self.date = date
		self.personResponsible = person
		self.event = event
		self.income = income
		self.expense = expense
		self.balance = balance

	def __repr__(self):
		return "<{}, {}, net:{}>".format(self.event, self.date, (self.income-self.expense))


class Coquitlam(db.Model):

	transactionID = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.Text, nullable=False)
	personResponsible = db.Column(db.String(25), nullable=False)
	event = db.Column(db.String(25), nullable=False)
	income = db.Column(db.Integer, nullable=False)
	expense = db.Column(db.Integer, nullable=False)
	balance = db.Column(db.Integer, nullable=False)

	def __init__(self, date, person, event, income, expense, balance):
		self.date = date
		self.personResponsible = person
		self.event = event
		self.income = income
		self.expense = expense
		self.balance = balance

	def __repr__(self):
		return "<{}, {}, net:{}>".format(self.event, self.date, (self.income-self.expense))


class Total(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	district = db.Column(db.String(15), nullable=False)
	id_district = db.Column(db.Integer, nullable=False)
	date = db.Column(db.Text, nullable=False)
	personResponsible = db.Column(db.String(25), nullable=False)
	event = db.Column(db.String(25), nullable=False)
	income = db.Column(db.Integer, nullable=False)
	expense = db.Column(db.Integer, nullable=False)
	balance = db.Column(db.Integer, nullable=False)

	def __init__(self, district, id_district, date, person, event, income, expense, balance):
		self.district = district
		self.id_district = id_district
		self.date = date
		self.personResponsible = person
		self.event = event
		self.income = income
		self.expense = expense
		self.balance = balance

	def __repr__(self):
		return "<From {}: {}, {}, net:{}>".format(self.district, self.event, self.date, (self.income-self.expense))