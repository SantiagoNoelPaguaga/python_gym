from flask import  Blueprint, jsonify,request  

from extensions import db, ma

from models.category_model import *

class CategorySchema(ma.Schema):
    class Meta:
        fields=('id','name')


category_schema=CategorySchema()            
categories_schema=CategorySchema(many=True)  

# Crear un Blueprint para la entidad Category
category_bp = Blueprint('categories', __name__)

# crea los endpoint o rutas (json)

#Obtener todos las categorías
@category_bp.route('/categories',methods=['GET'])
def get_categories():
    all_categories=Category.query.all()         
    result=categories_schema.dump(all_categories)                                     
    return jsonify(result)                    

#obtener la categoría que recibo por id
@category_bp.route('/categories/<id>',methods=['GET'])
def get_category(id):
    category=Category.query.get(id)
    return category_schema.jsonify(category)   

#Borrar la categoría que recibo por id
@category_bp.route('/categories/<id>',methods=['DELETE'])
def delete_category(id):
    category=Category.query.get(id)
    db.session.delete(category)

#Agregar una nueva categoría
@category_bp.route('/categories', methods=['POST'])
def add_category():
    data = request.get_json()
    category = Category(name=data['name'])
    db.session.add(category)
    db.session.commit()
    return jsonify({'Mensaje': 'La categoría se agregó correctamente!'})

@category_bp.route('/categories/<id>', methods=['PUT'])
def update_category(id):
    data = request.get_json()
    category = Category.query.get(id)
    category.name = data['name']
    db.session.commit()
    return jsonify({'Mensaje': 'La categoría se actualizó correctamente!'})