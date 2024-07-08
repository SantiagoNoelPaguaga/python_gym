from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from extensions import db

class User(db.Model):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(Text, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    image = Column(String(255), nullable=True)
    role = Column(String(50), nullable=False)

    transactions = relationship('Transaction', backref='user')

    def __init__(self, first_name, last_name, phone, address, email, username, password, image, role):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.address = address
        self.email = email
        self.username = username
        self.password = password
        self.image = image
        self.role = role