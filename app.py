from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuración de conexión a la base de datos
db_config = {
    'host': 'niconb994.mysql.pythonanywhere-services.com',
    'user': 'niconb994',
    'password': 'productos123',
    'database': 'niconb994$comercio'
}

@app.route('/productos', methods=['GET'])
def ver_productos():
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(productos)

@app.route('/eliminar_producto/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"mensaje": "REGISTRO ELIMINADO CON EXITO!!!"})

@app.route('/agregar_producto', methods=['POST'])
def crear_producto():
    info = request.json
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute("INSERT INTO productos(nombre,cantidad,precio) VALUES(%s,%s,%s)",
                   (info["nombre"], info["cantidad"], info["precio"]))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"mensaje": "REGISTRO CREADO CON EXITO!!!"})

@app.route('/actualizar_producto/<int:id>', methods=['PUT'])
def modificar_producto(id):
    info = request.json
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute("UPDATE productos SET nombre= %s, cantidad= %s, precio= %s WHERE id = %s",
                   (info["nombre"], info["cantidad"], info["precio"], id))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"mensaje": "PRODUCTO ACTUALIZADO CON EXITO!!!"})

if __name__ == '__main__':
