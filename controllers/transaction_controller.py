from flask import Blueprint, jsonify, request
from extensions import db, ma
from models.product_transaction_model import *
from models.transaction_model import *
from models.product_model import *
from sqlalchemy import func
from marshmallow import pre_dump

class ProductTransactionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_product', 'id_transaction', 'cantidad')

class SizeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')

def get_product_quantity(product, transaction):
    product_transaction = ProductTransaction.query.filter_by(id_product=product.id, id_transaction=transaction.id).first()
    return product_transaction.cantidad if product_transaction else None

class ProductSchema(ma.Schema):
    sizes = ma.Nested(SizeSchema, many=True)
    cantidad = ma.Method("get_cantidad")

    def get_cantidad(self, obj):
        # Obtén la transacción del contexto
        transaction = self.context.get('transaction', None)
        if transaction:
            return get_product_quantity(obj, transaction)
        return None

    class Meta:
        fields = ('id', 'image', 'name', 'description', 'price', 'stock', 'id_category', 'id_gender', 'sizes', 'cantidad')

class TransactionSchema(ma.Schema):
    products_transactions = ma.Nested(ProductTransactionSchema, many=True)
    products = ma.Method("get_products")

    class Meta:
        fields = ('id', 'date', 'id_user', 'products_transactions', 'products')

    def get_products(self, transaction):
        product_schema = ProductSchema()
        product_schema.context = {'transaction': transaction}
        return [product_schema.dump(product) for product in transaction.products]


transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
size_schema = SizeSchema()
sizes_schema = SizeSchema(many=True)

transaction_bp = Blueprint('transactions', __name__)

@transaction_bp.route('/transactions', methods=['GET'])
def get_transactions():
    all_transactions = Transaction.query.all()
    result = transactions_schema.dump(all_transactions, many=True)
    return jsonify(result)

@transaction_bp.route('/transactions/<int:id>', methods=['GET'])
def get_transaction(id):
    transaction = Transaction.query.get(id)
    if not transaction:
        return jsonify({'Mensaje': 'Transacción no encontrada'}), 404
    result = transaction_schema.dump(transaction)
    return jsonify(result)

# Crear una nueva transacción
@transaction_bp.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.json
    current_time = datetime.now()
    
    new_transaction = Transaction(
        date=current_time,
        id_user=data['id_user']
    )
    db.session.add(new_transaction)
    db.session.commit()

    products = data['products']
    for product in products:
        new_product_transaction = ProductTransaction(
            id_product=product['id_product'],
            id_transaction=new_transaction.id,
            cantidad=product['cantidad']
        )
        db.session.add(new_product_transaction)
    
    db.session.commit()
    return jsonify({'Mensaje': 'Compra realizada exitosamente!'})

# Eliminar una transacción
@transaction_bp.route('/transactions/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    transaction = Transaction.query.get(id)
    if not transaction:
        return jsonify({'Mensaje': 'Transacción no encontrada'}), 404

    ProductTransaction.query.filter_by(id_transaction=id).delete()
    db.session.delete(transaction)
    db.session.commit()
    return jsonify({'Mensaje': 'Transacción eliminada exitosamente'})

from sqlalchemy import func, extract

from sqlalchemy import func, extract

@transaction_bp.route('/transactions/total/day', methods=['GET'])
def total_sold_per_day():
    # Agrupar por día y calcular el total vendido sumando cantidad * precio
    result = db.session.query(func.date(Transaction.date).label('day'),
                              func.sum(ProductTransaction.cantidad * Product.price).label('total_sold')).\
             join(ProductTransaction).\
             join(Product).\
             group_by(func.date(Transaction.date)).all()

    # Formatear el resultado
    formatted_result = [{'day': row.day.strftime('%Y-%m-%d'), 'total_sold': row.total_sold} for row in result]

    return jsonify(formatted_result)

@transaction_bp.route('/transactions/total/month', methods=['GET'])
def total_sold_per_month():
    # Agrupar por mes y calcular el total vendido sumando cantidad * precio
    result = db.session.query(func.DATE_FORMAT(Transaction.date, '%Y-%m').label('month'),
                              func.sum(ProductTransaction.cantidad * Product.price).label('total_sold')).\
             join(ProductTransaction).\
             join(Product).\
             group_by(func.DATE_FORMAT(Transaction.date, '%Y-%m')).all()

    # Formatear el resultado
    formatted_result = [{'month': row.month, 'total_sold': row.total_sold} for row in result]

    return jsonify(formatted_result)

@transaction_bp.route('/transactions/total/year', methods=['GET'])
def total_sold_per_year():
    # Agrupar por año y calcular el total vendido sumando cantidad * precio
    result = db.session.query(func.DATE_FORMAT(Transaction.date, '%Y').label('year'),
                              func.sum(ProductTransaction.cantidad * Product.price).label('total_sold')).\
             join(ProductTransaction).\
             join(Product).\
             group_by(func.DATE_FORMAT(Transaction.date, '%Y')).all()

    # Formatear el resultado
    formatted_result = [{'year': row.year, 'total_sold': row.total_sold} for row in result]

    return jsonify(formatted_result)
