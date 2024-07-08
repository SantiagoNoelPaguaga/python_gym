import os
from flask import Flask

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Ruta de prueba para verificar que el servidor WSGI está funcionando
@app.route('/')
def hello():
    return "Hello World!"

# Punto de entrada para el servidor WSGI (Gunicorn u otro)
if __name__ == '__main__':
    app.run()
