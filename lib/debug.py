#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company, Dev, Freebie, Base

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create tables
    Base.metadata.create_all(engine)
    print("Database and tables created successfully.")

    # For debug: clear existing data (optional, comment out if you want persistent data)
    session.query(Freebie).delete()
    session.query(Dev).delete()
    session.query(Company).delete()
    session.commit()

    # Create some data
    company1 = Company(name="Google", founding_year=1998)
    company2 = Company(name="Amazon", founding_year=1994)

    dev1 = Dev(name="Alice")
    dev2 = Dev(name="Bob")

    session.add_all([company1, company2, dev1, dev2])
    session.commit()

    # Company gives freebies
    freebie1 = company1.give_freebie(dev1, "T-shirt", 10)
    freebie2 = company2.give_freebie(dev2, "Mug", 8)

    session.add_all([freebie1, freebie2])
    session.commit()

    # Test aggregate methods

    # 1. Freebie.print_details()
    print(freebie1.print_details())  # Expected: "Alice owns a T-shirt from Google."
    print(freebie2.print_details())  # Expected: "Bob owns a Mug from Amazon."

    # 2. Company.oldest_company()
    oldest = Company.oldest_company(session)
    print(f"The oldest company is: {oldest.name} (Founded {oldest.founding_year})")  # Amazon

    # 3. Dev.received_one()
    print(f"Has Alice received a 'T-shirt'? {dev1.received_one('T-shirt')}")  # True
    print(f"Has Bob received a 'T-shirt'? {dev2.received_one('T-shirt')}")    # False

    # 4. Dev.give_away()
    print(f"Before giveaway: {freebie1.print_details()}")  # Alice owns a T-shirt from Google
    dev1.give_away(dev2, freebie1)
    session.commit()
    print(f"After giveaway: {freebie1.print_details()}")   # Bob owns a T-shirt from Google

    session.close()

    print("Debugging complete.")
