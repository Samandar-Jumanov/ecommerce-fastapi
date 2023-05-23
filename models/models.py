from sqlalchemy import Column , String , Integer , Date, Boolean, ForeignKey, Float
from datetime import datetime
from helpers import Base
from sqlalchemy.orm import relationship


class UserModel(Base):
    __tablename__ ='users'
    id = Column(Integer, primary_key = True , index = True)
    username = Column(String , nullable = False )
    email = Column(String , nullable = False , unique = True  )
    password = Column(String , nullable = False )
    joined_date = Column(Date, default=datetime.utcnow)
    products = relationship('Product', back_populates='owner')
    payment  = relationship('Payments', back_populates='client')


class Product(Base):
    __tablename__ = 'products' 
    id = Column(Integer, primary_key = True , index = True)
    product_name = Column(String , nullable = False)
    product_image = Column(String, nullable = False)
    product_description = Column(String , nullable = False )
    product_price = Column(Integer , nullable = False)
    owner_location = Column(String , default = False )
    added_date = Column(Date, default=datetime.utcnow)
    owner_id = Column(Integer , ForeignKey('users.id'))
    owner = relationship('UserModel', back_populates='products')


class Payments(Base):
    __tablename__ = 'payments'
    id = Column(Integer , primary_key = True )
    amount = Column(Float)
    currency = Column(String)
    description = Column(String)
    paid = Column(Date)
    stripe_id = Column(String)
    clinet_id = Column(Integer , ForeignKey('users.id'))
    client = relationship('UserModel', back_populates='payment')




 
    





