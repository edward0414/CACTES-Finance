from app import db
from models import *

# create the database and the db tables
db.create_all()


# insert
db.session.add(Coquitlam("2017-09-17", "Edward Feng", "Initial", 0, 0, 0))
db.session.add(Delta("2017-09-17", "Edward Feng", "Initial", 0, 0, 0))
db.session.add(Surrey("2017-09-17", "Edward Feng", "Initial", 0, 0, 0))
db.session.add(Vancouver("2017-09-17", "Edward Feng", "Initial", 0, 0, 0))
db.session.add(Total("No District", 0, "2017-09-17", "Edward Feng", "Initial", 0, 0, 0))
db.session.add(Staff("Edward", "Feng", "admin@admin", "admin", "University of Toronto", "Treasurer"))


# commit the changes
db.session.commit()