from flask import  Blueprint, jsonify,request  

from extensions import db, ma

from models.size_model import *

class SizeSchema(ma.Schema):
    class Meta:
        fields=('id','name')

size_schema=SizeSchema()            
sizes_schema=SizeSchema(many=True)  

# Crear un Blueprint para la entidad Size
size_bp = Blueprint('sizes', __name__)

# crea los endpoint o rutas (json)

#Obtener todos los sizes
@size_bp.route('/sizes',methods=['GET'])
def get_sizes():
    all_sizes=Size.query.all()         
    result=sizes_schema.dump(all_sizes)                                     
    return jsonify(result)                    

#obtener el size que recibo por id
@size_bp.route('/sizes/<id>',methods=['GET'])
def get_size(id):
    size=Size.query.get(id)
    return size_schema.jsonify(size)   

#Borrar el size que recibo por id
@size_bp.route('/sizes/<id>',methods=['DELETE'])
def delete_size(id):
    size=Size.query.get(id)
    db.session.delete(size)

#Agregar un nuevo size
@size_bp.route('/sizes', methods=['POST'])
def add_size():
    data = request.get_json()
    size = Size(name=data['name'])
    db.session.add(size)
    db.session.commit()
    return jsonify({'Mensaje': 'El talle se agregó correctamente!'})

@size_bp.route('/sizes/<id>', methods=['PUT'])
def update_size(id):
    data = request.get_json()
    size = Size.query.get(id)
    size.name = data['name']
    db.session.commit()
    return jsonify({'Mensaje': 'El talle se actualizó correctamente!'})