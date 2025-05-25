
from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Naming convention for foreign keys
convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

# Base declarative class
Base = declarative_base(metadata=metadata)

# Company class
class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())  
    founding_year = Column(Integer())
    freebies = relationship('Freebie', back_populates='company')

    def __repr__(self):
        return f'<Company {self.name}>'

    def give_freebie(self, dev, item_name, value):
        """Creates a new Freebie instance associated with this company and the given dev."""
        return Freebie(name=item_name, value=value, dev=dev, company=self)

    @classmethod
    def oldest_company(cls, session):
        """Returns the Company instance with the earliest founding year."""
        return session.query(cls).order_by(cls.founding_year.asc()).first()

# Dev class
class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())
    freebies = relationship('Freebie', back_populates='dev')

    def __repr__(self):
        return f'<Dev {self.name}>'

    def received_one(self, item_name):
        """Returns True if any of the dev's freebies has the given item_name."""
        return any(freebie.name == item_name for freebie in self.freebies)

    def give_away(self, other_dev, freebie):
        """
        Transfers ownership of a freebie to another dev,
        only if this dev currently owns the freebie.
        """
        if freebie.dev == self:
            freebie.dev = other_dev

# Freebie class
class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())  # rename from item_ to name
    value = Column(Integer())  
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    company_id = Column(Integer(), ForeignKey('companies.id'))

    dev = relationship('Dev', back_populates='freebies', cascade='save-update,merge')
    company = relationship('Company', back_populates='freebies', cascade='save-update,merge')

    def __repr__(self):
        return f'<Freebie {self.name}>'

    def print_details(self):
        return f"{self.dev.name} owns a {self.name} from {self.company.name}."
    