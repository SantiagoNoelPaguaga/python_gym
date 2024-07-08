from sqlalchemy import Column, Integer, ForeignKey

from extensions import db

class ProductTransaction(db.Model):
    __tablename__ = 'Products_Transactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_product = Column(Integer, ForeignKey('Products.id'), nullable=False)
    id_transaction = Column(Integer, ForeignKey('Transaction.id'), nullable=False)
    cantidad = Column(Integer, nullable=False)

    def __init__(self, id_product, id_transaction, cantidad):
        self.id_product = id_product
        self.id_transaction = id_transaction
        self.cantidad = cantidad