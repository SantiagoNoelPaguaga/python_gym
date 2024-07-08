from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from extensions import db

class Transaction(db.Model):
    __tablename__ = 'Transaction'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    id_user = Column(Integer, ForeignKey('Users.id'), nullable=False)

    product_transactions = relationship('ProductTransaction', backref='transaction')
    products = relationship('Product', secondary='Products_Transactions', backref='transaction')
    
    def __init__(self, date, id_user):
        self.date = date
        self.id_user = id_user