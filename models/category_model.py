from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from extensions import db 

class Category(db.Model):
    __tablename__ = 'Categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    products = relationship('Product', backref='category')
    
    def __init__(self, name):
        self.name = name