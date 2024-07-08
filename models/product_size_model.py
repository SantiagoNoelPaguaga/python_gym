from sqlalchemy import Column, Integer, ForeignKey

from extensions import db

class ProductSize(db.Model):
    __tablename__ = 'Products_Sizes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_product = Column(Integer, ForeignKey('Products.id'), nullable=False)
    id_size = Column(Integer, ForeignKey('Sizes.id'), nullable=False)

    def __init__(self, id_product, id_size):
        self.id_product = id_product
        self.id_size = id_size
