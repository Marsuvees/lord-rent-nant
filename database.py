from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import os
from urllib import parse
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Create a SQLAlchemy engine and session
try:
    username = "marsuvees"
    password = parse.quote(os.environ.get('MARSUVEES_PSQL_PASS'))
    host = "localhost"
    port = 5432
    database = "rent_reminder_system"
    engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')  # Use your desired database connection URL
except:
    print('Dropping to SQLite')
    engine = create_engine('sqlite:///rent_reminder_system.db')
Session = sessionmaker(bind=engine)
session = Session()

# Define the base for declarative class definitions
Base = declarative_base()

# Define the Landlord table
class Users(Base):
    __tablename__ = 'landlords'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

# Define tenant table
class Tenants(Base):
    __tablename__ = 'tenants'
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False)
    landlord_id = Column(Integer, ForeignKey('landlords.id'), nullable=False)
    landlord = relationship(Users, backref='tenants')
    paid_rent = Column(Boolean, default = False)

    # Define method to change paid rent status
    def change_paid_rent_status(self):
        if self.paid_rent == False:
            self.paid_rent = True
        else:
            self.paid_rent = False
        return self.paid_rent

            


# Define the House table
class Property(Base):
    __tablename__ = 'properties'
    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    description = Column(String, default = None)
    rent = Column(Integer, default = None, nullable=False)
    date_leased = Column(Date, nullable=True)
    landlord_id = Column(Integer, ForeignKey('landlords.id'))
    landlord = relationship(Users, backref='properties')
    status = Column(Boolean, default = False)
    current_occupant_id = Column(Integer, ForeignKey('tenants.id'), nullable=True)
    rent_expiry_date = Column(Date, nullable=True, default=None)
    tenant = relationship(Tenants, backref='properties')

    # Define method to assign new tenant
    def assign_tenant(self, tenant_id):
        if self.current_occupant_id == None:
            self.current_occupant_id = tenant_id
            self.status = True
        else:
            self.current_occupant_id = None
            self.status = False

    # Define method to change status
    def change_status(self):
        if self.current_occupant_id == None:
            self.status = False
        else:
            self.status = True

    # Define method to assign new rent expiry date
    def assign_expiry_date(self, rent_period):
        if self.date_leased == None:
            self.rent_expiry_date = None
            return 'Lease and rent dates not set'
        else:
            self.rent_expiry_date = self.date_leased + relativedelta(months=rent_period)
            return 'Lease and rent dates set'

if __name__ == '__main__': 
    # Create the tables in the database
    Base.metadata.create_all(engine)

    # Create admin password hasher
    from bcrypt import hashpw, gensalt
    salt = gensalt()

    # Enter admin data into the database
    admin = Users(name="admin", email="tolujed@gmail.com", password=hashpw("random_shit".encode('utf-8'), salt).decode('utf-8'))
    test_tenant = Tenants(full_name="James Jed", email="tolujed@gmail.com", phone_number="1234567890", landlord_id=1)
    test_house = Property(description='2 bedrooms \n4 kitchens \n3 balconies',address="12345 Test Street", landlord_id=1, rent = 100000, current_occupant_id=1)
    test_house.assign_expiry_date(6)
    test_house.change_status()
    session.add_all([admin, test_tenant, test_house,])
    # update_query = session.query(Houses).filter(Houses.id == 1).first()
    # update_query.tenant_id = None
    session.commit()

    # Close the session when done
    session.close()
    
