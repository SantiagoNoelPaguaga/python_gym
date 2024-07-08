from flask import  Blueprint, jsonify,request  

from extensions import db, ma

from models.gender_model import *

class GenderSchema(ma.Schema):
    class Meta:
        fields=('id','name')


gender_schema=GenderSchema()            
genders_schema=GenderSchema(many=True)  

# Crear un Blueprint para la entidad Gender
gender_bp = Blueprint('genders', __name__)

# crea los endpoint o rutas (json)

#Obtener todos los géneros
@gender_bp.route('/genders',methods=['GET'])
def get_genders():
    all_genders=Gender.query.all()         
    result=genders_schema.dump(all_genders)                                     
    return jsonify(result)                    

#obtener el género que recibo por id
@gender_bp.route('/genders/<id>',methods=['GET'])
def get_gender(id):
    gender=Gender.query.get(id)
    return gender_schema.jsonify(gender)   

#Borrar el género que recibo por id
@gender_bp.route('/genders/<id>',methods=['DELETE'])
def delete_gender(id):
    gender=Gender.query.get(id)
    db.session.delete(gender)

#Agregar un nuevo género
@gender_bp.route('/genders', methods=['POST'])
def add_gender():
    data = request.get_json()
    gender = Gender(name=data['name'])
    db.session.add(gender)
    db.session.commit()
    return jsonify({'Mensaje': 'El género se agregó correctamente!'})

@gender_bp.route('/genders/<id>', methods=['PUT'])
def update_gender(id):
    data = request.get_json()
    gender = Gender.query.get(id)
    gender.name = data['name']
    db.session.commit()
    return jsonify({'Mensaje': 'El género se actualizó correctamente!'})