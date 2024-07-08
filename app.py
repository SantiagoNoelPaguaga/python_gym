import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask import Flask
from flask_cors import CORS
from extensions import db, ma  # Importar desde extensions.py

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False)

db.init_app(app)
ma.init_app(app)

cloudinary.config(
    cloud_name='dtyjjes5z',  # Reemplaza 'tu_cloud_name' con tu Cloudinary cloud name
    api_key='284231559873866',        # Reemplaza 'tu_api_key' con tu Cloudinary API key
    api_secret='yjO5n3_0p4hPqtCe4YTK-K27Eqk',  # Reemplaza 'tu_api_secret' con tu Cloudinary API secret
    api_proxy = "http://proxy.server:3128"
)

# Importar los modelos después de inicializar db y ma
with app.app_context():
    from models import Category, Gender, Size, Product, ProductSize, User, Transaction, ProductTransaction
    db.create_all()

# Importar y registrar los Blueprints
from controllers.gender_controller import gender_bp
app.register_blueprint(gender_bp, url_prefix='/api')
from controllers.category_controller import category_bp
app.register_blueprint(category_bp, url_prefix='/api')
from controllers.size_controller import size_bp
app.register_blueprint(size_bp, url_prefix='/api')
from controllers.user_controller import user_bp
app.register_blueprint(user_bp, url_prefix='/api')
from controllers.product_controller import product_bp
app.register_blueprint(product_bp, url_prefix='/api')
from controllers.transaction_controller import transaction_bp
app.register_blueprint(transaction_bp, url_prefix='/api')

# Programa principal
if __name__ == '__main__':
    app.run(debug=True, port=5000)
