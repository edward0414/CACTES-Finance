from app import db
from models import *

# create the database and the db tables
db.create_all()


# insert
db.session.add(Staff("Edward", "Feng", "admin@admin", "admin", "Senior", "All", "Treasurer", "University of Toronto"))
db.session.add(Staff("Lance", "Wang", "lance.wang@cactesassociation.org", "lance", "Senior", "All", "Director of Finance", "Earl Marriott Secondary"))

db.session.add(Transaction("Coquitlam","2017-10-22", "Edward Feng", "Edward Feng", "Initiated", 0, 0, "Edward Feng", '2017-10-30 14:41:35 PDT'))
db.session.add(Transaction("Delta","2017-10-22", "Edward Feng", "Edward Feng","Initiated", 0, 0, "Edward Feng", '2017-10-30 14:41:35 PDT'))
db.session.add(Transaction("Surrey","2017-10-22", "Edward Feng", "Edward Feng","Initiated", 0, 0, "Edward Feng", '2017-10-30 14:41:35 PDT'))
db.session.add(Transaction("Vancouver","2017-10-22", "Edward Feng", "Edward Feng", "Initiated", 0, 0, "Edward Feng", '2017-10-30 14:41:35 PDT'))
db.session.add(Transaction("Administration", "2017-10-22", "Edward Feng", "Edward Feng", "Initiated", 0, 0, "Edward Feng", '2017-10-30 14:41:35 PDT'))
db.session.add(MoneyCount("Income", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1))
db.session.add(MoneyCount("Expense", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1))
db.session.add(MoneyCount("Income", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2))
db.session.add(MoneyCount("Expense", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2))
db.session.add(MoneyCount("Income", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3))
db.session.add(MoneyCount("Expense", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3))
db.session.add(MoneyCount("Income", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4))
db.session.add(MoneyCount("Expense", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4))
db.session.add(MoneyCount("Income", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5))
db.session.add(MoneyCount("Expense", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5))


# commit the changes
db.session.commit()