#!/usr/bin/env python3

from models import Dev, Company, Freebie
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()
# Seed the database with initial data
# This script populates the database with initial data for testing purposes.
# Ensure the database and tables are created
from models import Base

Base.metadata.create_all(engine)
# Import necessary models
# from models import Dev, Company, Freebie
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine
# Create a new session  
# Clear tables if needed
session.query(Freebie).delete()
session.query(Dev).delete()
session.query(Company).delete()

company1 = Company(name="Google", founding_year=1998)
company2 = Company(name="Amazon", founding_year=1994)

dev1 = Dev(name="Alice")
dev2 = Dev(name="Bob")

freebie1 = Freebie(name="T-shirt", dev=dev1, company=company1)
freebie2 = Freebie(name="Mug", dev=dev2, company=company2)

session.add_all([company1, company2, dev1, dev2, freebie1, freebie2])
session.commit()
# Commit the session to save the changes
session.close()

print("Database seeded successfully with the initial data")
