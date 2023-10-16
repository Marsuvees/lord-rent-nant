from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from urllib import parse
import os
from datetime import datetime

# Create a SQLAlchemy engine and session
username = "marsuvees"
password = "987654321"
host = "localhost"
port = 5432
database = "rent_reminder_system"
engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')  # Use your desired database connection URL
Session = sessionmaker(bind=engine)
session = Session()

# Define the base for declarative class definitions
Base = declarative_base()

# Define the Landlord table
class Landlords(Base):
    __tablename__ = 'landlords'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

# Define the Tenant table
class Tenants(Base):
    __tablename__ = 'tenants'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

# Define the House table
class Houses(Base):
    __tablename__ = 'houses'
    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    date_leased = Column(Date, default = None)
    landlord_id = Column(Integer, ForeignKey('landlords.id'))
    tenant_id = Column(Integer, ForeignKey('tenants.id'))
    landlord = relationship(Landlords, backref='houses')
    tenant = relationship(Tenants, backref='houses')

if __name__ == '__main__': 
    # Create the tables in the database
    Base.metadata.create_all(engine)

    # Enter admin data into the database
    admin_l = Landlords(name="admin", email="tolujed@gmail.com", password="random_shit")
    admin_t = Tenants(name="admin", email="tolujed@gmail.com", password="random_shit")
    test_house = Houses(address="12345 Test Street", landlord_id=1, tenant_id=1, date_leased=datetime.today())
    session.add_all([admin_t, admin_l, test_house,])
    # update_query = session.query(Houses).filter(Houses.id == 1).first()
    # update_query.tenant_id = None
    session.commit()

    # Close the session when done
    session.close()
    
    print(datetime.today().date())