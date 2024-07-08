from sqlalchemy import Column, Integer, String, Text, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship

from extensions import db 

class Product(db.Model):
    __tablename__ = 'Products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    image = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    stock = Column(Integer, nullable=False)
    id_category = Column(Integer, ForeignKey('Categories.id'), nullable=False)
    id_gender = Column(Integer, ForeignKey('Genders.id'), nullable=False)

    product_sizes = relationship('ProductSize', backref='product')
    product_transactions = relationship('ProductTransaction', backref='product')
    sizes = relationship('Size', secondary='Products_Sizes', backref='products')

    def __init__(self, image, name, description, price, stock, id_category, id_gender):
        self.image = image
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.id_category = id_category
        self.id_gender = id_gender
