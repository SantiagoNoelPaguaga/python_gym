from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from extensions import db

class Size(db.Model):
    __tablename__ = 'Sizes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    products_sizes = relationship('ProductSize', backref='size')

    def __init__(self, name):
        self.name = name