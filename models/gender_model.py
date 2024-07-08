from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from extensions import db

class Gender(db.Model):
    __tablename__ = 'Genders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    products = relationship('Product', backref='gender')

    def __init__(self, name):
        self.name = name