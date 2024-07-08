from flask import Blueprint, jsonify, request
import cloudinary.uploader
from extensions import db, ma
from models.product_model import *
from models.product_size_model import *
from sqlalchemy.orm import joinedload

class SizeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')

class ProductSchema(ma.Schema):
    sizes = ma.Nested(SizeSchema, many=True)
    class Meta:
        fields = ('id', 'image', 'name', 'description', 'price', 'stock', 'id_category', 'id_gender', 'sizes')
        
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
size_schema = SizeSchema()
sizes_schema = SizeSchema(many=True)

product_bp = Blueprint('products', __name__)

# Obtener todos los productos
@product_bp.route('/products', methods=['GET'])
def get_products():
    all_products = Product.query.options(joinedload(Product.sizes)).all()
    result = products_schema.dump(all_products)
    return jsonify(result)

# Obtener producto por id
@product_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

# Borrar producto por id
@product_bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'Mensaje': 'Producto no encontrado'}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({'Mensaje': 'Producto eliminado'})

# Agregar un nuevo producto
@product_bp.route('/products', methods=['POST'])
def add_product():
    data = request.form
    image = request.files['image']

    result = cloudinary.uploader.upload(image)
    image_url = result['secure_url']

    new_product = Product(
        image=image_url,
        name=data['name'],
        description=data['description'],
        price=data['price'],
        stock=data['stock'],
        id_category=data['id_category'],
        id_gender=data['id_gender']
    )
    db.session.add(new_product)
    db.session.commit()

    sizes = data.getlist('sizes')
    for size_id in sizes:
        product_size = ProductSize(id_product=new_product.id, id_size=size_id)
        db.session.add(product_size)

    db.session.commit()
    return jsonify({'Mensaje': 'Producto agregado exitosamente!'})

# Actualizar un producto
@product_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'Mensaje': 'Producto no encontrado'}), 404

    data = request.form

    if 'image' in request.files:
        image = request.files['image']
        result = cloudinary.uploader.upload(image)
        product.image = result['secure_url']

    if 'name' in data:
        product.name = data['name']
    if 'description' in data:
        product.description = data['description']
    if 'price' in data:
        product.price = data['price']
    if 'stock' in data:
        product.stock = data['stock']
    if 'id_category' in data:
        product.id_category = data['id_category']
    if 'id_gender' in data:
        product.id_gender = data['id_gender']

    sizes = data.getlist('sizes')
    if sizes:
        ProductSize.query.filter_by(id_product=product_id).delete()
        for size_id in sizes:
            product_size = ProductSize(id_product=product_id, id_size=size_id)
            db.session.add(product_size)

    db.session.commit()
    return jsonify({'Mensaje': 'Producto actualizado exitosamente!'})
