from flask import Flask, request, jsonify, render_template
from flask import request
from flask_cors import CORS
import mysql.connector
from werkzeug.utils import secure_filename
import os
import time
#--------------------------------------------------------------------

app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas
        
#--------------------------------------------------------------------
class Pedidos:
    #----------------------------------------------------------------
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()

        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        # Una vez que la base de datos está establecida, creamos la tabla si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
            `idCliente` int(11) NOT NULL AUTO_INCREMENT,
            `nombre` varchar(50) NOT NULL,
            `apellido` varchar(50) NOT NULL,
            `telefono` varchar(20) NOT NULL,
            `email` varchar(50) NOT NULL,
            `direccion` varchar(50) NOT NULL,
            `cp` varchar(50) NOT NULL,
            PRIMARY KEY (`idCliente`), UNIQUE KEY `email` (`email`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;''')
        self.conn.commit()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
            codigo INT AUTO_INCREMENT PRIMARY KEY,
            descripcion VARCHAR(255) NOT NULL,
            cantidad INT NOT NULL,
            precio DECIMAL(10, 2) NOT NULL,
            imagen_url VARCHAR(255),
            proveedor INT(4))''')
        self.conn.commit()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS pedidos (
            `idPedido` INT(11) NOT NULL AUTO_INCREMENT , 
            `idCliente` INT(11) NOT NULL , 
            `idCafe` INT(11) NOT NULL DEFAULT '0' , 
            `cantidadCafe` INT(11) NOT NULL DEFAULT '0' , 
            `idComidas` VARCHAR(50) NOT NULL DEFAULT '0' , 
            `total` INT(11) NOT NULL DEFAULT '0' , 
            `modoPago` TINYINT(1) NOT NULL DEFAULT '1' , 
            `comentario` VARCHAR(150) NOT NULL , 
            PRIMARY KEY (`idPedido`)) ENGINE = InnoDB;''')
        self.conn.commit()


#        #Añadimos productos hardcodeados si la tabla productos esta vacia.
#        self.cursor.execute("SELECT COUNT(*) FROM productos;")
#        if self.cursor.fetchone()[0] == 0:
#            self.cursor.execute('''INSERT INTO `productos`(`nombre`, `tipo`, `stock`, `precio`, `estado`) VALUES
#                                ('Espresso','1','5','500','1'),
#                                ('Americano','1','0','1500','1'),
#                                ('Cortado','1','2','200','1'),
#                                ('Macchiato','1','4','300','1'),
#                                ('Lagrima','1','50','700','1'),
#                                ('Capuchino','1','10','800','1');''')
#            self.conn.commit()

        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)
        
#----------------------------------------------------------------
#Clientes
#----------------------------------------------------------------
    def agregar_cliente(self, nombre, apellido, telefono, email, direccion, cp):
        sql = """INSERT INTO clientes (nombre, apellido, telefono, email, direccion, cp)
          VALUES (%s, %s, %s, %s, %s, %s)"""
        valores = (nombre, apellido, telefono, email, direccion, cp)

        self.cursor.execute(sql, valores)        
        self.conn.commit()
        return self.cursor.lastrowid

    def consultar_cliente(self, email):
        self.cursor.execute(f"SELECT * FROM clientes WHERE email = '{email}'")
        return self.cursor.fetchone()
    
    def modificar_cliente(self, email, n_nombre, n_apellido, n_telefono, n_direccion, n_cp):
        sql = "UPDATE clientes SET nombre = %s, apellido = %s, telefono = %s, direccion = %s, cp = %s WHERE email = %s"
        valores = (n_nombre, n_apellido, n_telefono, n_direccion, n_cp, email)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def listar_clientes(self):
        self.cursor.execute("SELECT * FROM clientes")
        clientes = self.cursor.fetchall()
        return clientes
    
    def eliminar_cliente(self, email):
        self.cursor.execute(f"DELETE FROM productos WHERE email = {email}")
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def mostrar_cliente(self, email):
        cliente = self.consultar_cliente(email)
        if cliente:
            print("-" * 40)
            print(f"Nombre.....: {cliente['nombre']}")
            print(f"Apellido: {cliente['apellido']}")
            print(f"Telefono...: {cliente['telefono']}")
            print(f"Email.....: {cliente['email']}")
            print(f"Dirección.....: {cliente['direccion']}")
            print(f"Codigo Postal..: {cliente['cp']}")
            print("-" * 40)
        else:
            print("Cliente no encontrado.")

#----------------------------------------------------------------
#Productos
#----------------------------------------------------------------
    def agregar_producto(self, descripcion, cantidad, precio, imagen, proveedor):
               
        sql = """INSERT INTO productos (descripcion, cantidad, precio, imagen_url, proveedor)
          VALUES (%s, %s, %s, %s, %s)"""
        valores = (descripcion, cantidad, precio, imagen, proveedor)

        self.cursor.execute(sql, valores)        
        self.conn.commit()
        return self.cursor.lastrowid
#----------------------------------------------------------------
    def consultar_producto(self, codigo):
        # Consultamos un producto a partir de su código
        self.cursor.execute(f"SELECT * FROM productos WHERE codigo = {codigo}")
        return self.cursor.fetchone() #Me da el diccionario o None si no existe
 #----------------------------------------------------------------
    def modificar_producto(self, codigo, nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_imagen, nuevo_proveedor):
        sql = "UPDATE productos SET descripcion = %s, cantidad = %s, precio = %s, imagen_url = %s, proveedor = %s WHERE codigo = %s"
        valores = (nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_imagen, nuevo_proveedor, codigo)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0
#----------------------------------------------------------------
    def listar_productos(self):
        self.cursor.execute("SELECT * FROM productos")
        productos = self.cursor.fetchall()
        return productos
#----------------------------------------------------------------
    def eliminar_producto(self, codigo):
        # Eliminamos un producto de la tabla a partir de su código
        self.cursor.execute(f"DELETE FROM productos WHERE codigo = {codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0
#----------------------------------------------------------------
    def mostrar_producto(self, codigo):
        # Mostramos los datos de un producto a partir de su código
        producto = self.consultar_producto(codigo)
        if producto:
            print("-" * 40)
            print(f"Código.....: {producto['codigo']}")
            print(f"Descripción: {producto['descripcion']}")
            print(f"Cantidad...: {producto['cantidad']}")
            print(f"Precio.....: {producto['precio']}")
            print(f"Imagen.....: {producto['imagen_url']}")
            print(f"Proveedor..: {producto['proveedor']}")
            print("-" * 40)
        else:
            print("Producto no encontrado.")
#----------------------------------------------------------------   
#Pedidos
#----------------------------------------------------------------     
    def agregar_pedido(self, idcliente, idcafe, cantcafe, idcomidas, total, modopago, comentario):
               
        sql = """INSERT INTO pedidos (idCliente, idCafe, cantidadCafe, idComidas, total, modoPago, comentario)
          VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        valores = (idcliente, idcafe, cantcafe, idcomidas, total, modopago, comentario)

        self.cursor.execute(sql, valores)        
        self.conn.commit()
        return self.cursor.lastrowid
#----------------------------------------------------------------
    def consultar_pedido(self, codigo):
        # Consultamos un producto a partir de su código
        self.cursor.execute(f"SELECT * FROM pedidos WHERE idPedido = {codigo}")
        return self.cursor.fetchone() #Me da el diccionario o None si no existe
#----------------------------------------------------------------
    def modificar_pedidos(self, codigo, n_idcliente, n_idcafe, n_cantcafe, n_comidas, n_total, n_modpago, n_comentario):
        sql = "UPDATE pedidos SET idCliente = %s, idCafe = %s, cantidadCafe = %s, idComidas = %s, total = %s, modoPago = %s, comentario = %s WHERE idPedido = %s"
        valores = (n_idcliente, n_idcafe, n_cantcafe, n_comidas, n_total, n_modpago, n_comentario, codigo)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0
#----------------------------------------------------------------
    def listar_pedidos(self):
        self.cursor.execute("SELECT * FROM pedidos")
        pedidos = self.cursor.fetchall()
        return pedidos
#----------------------------------------------------------------
    def eliminar_pedidos(self, codigo):
        # Eliminamos un producto de la tabla a partir de su código
        self.cursor.execute(f"DELETE FROM pedidos WHERE idPedido = {codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0
#----------------------------------------------------------------
    def mostrar_pedido(self, codigo):
        # Mostramos los datos de un producto a partir de su código
        pedido = self.consultar_pedido(codigo)
        if pedido:
            print("-" * 40)
            print(f"Código.....: {pedido['idPedido']}")
            print(f"Id Cliente.....: {pedido['idCliente']}")
            print(f"Id Cafe: {pedido['idCafe']}")
            print(f"Cantidad...: {pedido['cantidadCafe']}")
            print(f"Comida.....: {pedido['idComidas']}")
            print(f"Total.....: {pedido['total']}")
            print(f"Modo de Pago..: {pedido['modoPago']}")
            print(f"Comentario..: {pedido['comentario']}")
            print("-" * 40)
        else:
            print("Pedido no encontrado.")

#--------------------------------------------------------------------
# Cuerpo del programa
#--------------------------------------------------------------------
# Carpeta para guardar las imagenes.
RUTA_DESTINO = '/home/rodriv33/mysite/CRUD/static/imagenes/'

#Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
#RUTA_DESTINO = '/home/USUARIO/mysite/static/imagenes'

# Crear una instancia de la clase pedidos
pedidos = Pedidos(host='rodriv33.mysql.pythonanywhere-services.com', user='rodriv33', password='pycoffe_33', database='rodriv33$pythoncoffe')
#pedidos = pedidos(host='USUARIO.mysql.pythonanywhere-services.com', user='USUARIO', password='CLAVE', database='USUARIO$miapp')

#--------------------------------------------------------------------
# Listar todos los clientes
#--------------------------------------------------------------------
@app.route("/clientes", methods=["GET"])
def listar_pedclientes():
    clientes = pedidos.listar_clientes()
    return jsonify(clientes)
#--------------------------------------------------------------------
# Mostrar un sólo cliente según su email
#--------------------------------------------------------------------
@app.route("/clientes/<string:email>", methods=["GET"])
def mostrar_pedcliente(email):
    cliente = pedidos.consultar_cliente(email)
    if cliente:
        return jsonify(cliente), 201
    else:
        return "Cliente no encontrado", 404
#--------------------------------------------------------------------
# Agregar un cliente
#--------------------------------------------------------------------
@app.route("/clientes", methods=["POST"])
def agregar_pedcliente():
    #Recojo los datos del form
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    telefono = request.form['telefono']
    email = request.form['correo']
    direccion = request.form['calle']  
    cp= request.form['cp']

    nuevo_codigo = pedidos.agregar_cliente(nombre, apellido, telefono, email, direccion, cp)
    if nuevo_codigo:    
        #Si el producto se agrega con éxito, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 201 (Creado).
        return jsonify({"mensaje": "Cliente agregado correctamente.", "codigo": nuevo_codigo}), 201
    else:
        #Si el producto no se puede agregar, se devuelve una respuesta JSON con un mensaje de error y un código de estado HTTP 500 (Internal Server Error).
        return jsonify({"mensaje": "Error al agregar el Cliente."}), 500    
#--------------------------------------------------------------------
#--------------------------------------------------------------------
# Modificar un cliente según su email
#--------------------------------------------------------------------
@app.route("/clientes/<string:email>", methods=["PUT"])
def modificar_pedcliente(email):
    #Se recuperan los nuevos datos del formulario
    n_nombre = request.form.get("nombre")
    n_apellido = request.form.get("apellido")
    n_telefono = request.form.get("telefono")
    n_direccion = request.form.get("calle")
    n_cp = request.form.get("cp")

    if pedidos.modificar_cliente(email, n_nombre, n_apellido, n_telefono, n_direccion, n_cp):
        return jsonify({"mensaje": "Cliente modificado"}), 200
    else:
        return jsonify({"mensaje": "Cliente no encontrado"}), 404
#--------------------------------------------------------------------
# Listar todos los productos
#--------------------------------------------------------------------
#La ruta Flask /productos con el método HTTP GET está diseñada para proporcionar los detalles de todos los productos almacenados en la base de datos.
#El método devuelve una lista con todos los productos en formato JSON.
@app.route("/productos", methods=["GET"])
def listar_productos():
    productos = pedidos.listar_productos()
    return jsonify(productos)
#--------------------------------------------------------------------
# Mostrar un sólo producto según su código
#--------------------------------------------------------------------
#La ruta Flask /productos/<int:codigo> con el método HTTP GET está diseñada para proporcionar los detalles de un producto específico basado en su código.
#El método busca en la base de datos el producto con el código especificado y devuelve un JSON con los detalles del producto si lo encuentra, o None si no lo encuentra.
@app.route("/productos/<int:codigo>", methods=["GET"])
def mostrar_producto(codigo):
    producto = pedidos.consultar_producto(codigo)
    if producto:
        return jsonify(producto), 201
    else:
        return "Producto no encontrado", 404
#--------------------------------------------------------------------
# Agregar un producto
#--------------------------------------------------------------------
@app.route("/productos", methods=["POST"])
#La ruta Flask `/productos` con el método HTTP POST está diseñada para permitir la adición de un nuevo producto a la base de datos.
#La función agregar_producto se asocia con esta URL y es llamada cuando se hace una solicitud POST a /productos.
def agregar_producto():
    #Recojo los datos del form
    descripcion = request.form['descripcion']
    cantidad = request.form['cantidad']
    precio = request.form['precio']
    imagen = request.files['imagen']
    proveedor = request.form['proveedor']  
    nombre_imagen=""

    
    # Genero el nombre de la imagen
    nombre_imagen = secure_filename(imagen.filename) #Chequea el nombre del archivo de la imagen, asegurándose de que sea seguro para guardar en el sistema de archivos
    nombre_base, extension = os.path.splitext(nombre_imagen) #Separa el nombre del archivo de su extensión.
    nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}" #Genera un nuevo nombre para la imagen usando un timestamp, para evitar sobreescrituras y conflictos de nombres.

    nuevo_codigo = pedidos.agregar_producto(descripcion, cantidad, precio, nombre_imagen, proveedor)
    if nuevo_codigo:    
        imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))
        print("Se guardo!")
        #Si el producto se agrega con éxito, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 201 (Creado).
        return jsonify({"mensaje": "Producto agregado correctamente.", "codigo": nuevo_codigo, "imagen": nombre_imagen}), 201
    else:
        #Si el producto no se puede agregar, se devuelve una respuesta JSON con un mensaje de error y un código de estado HTTP 500 (Internal Server Error).
        return jsonify({"mensaje": "Error al agregar el producto."}), 500
    

#--------------------------------------------------------------------
# Modificar un producto según su código
#--------------------------------------------------------------------
@app.route("/productos/<int:codigo>", methods=["PUT"])
#La ruta Flask /productos/<int:codigo> con el método HTTP PUT está diseñada para actualizar la información de un producto existente en la base de datos, identificado por su código.
#La función modificar_producto se asocia con esta URL y es invocada cuando se realiza una solicitud PUT a /productos/ seguido de un número (el código del producto).
def modificar_producto(codigo):
    #Se recuperan los nuevos datos del formulario
    nueva_descripcion = request.form.get("descripcion")
    nueva_cantidad = request.form.get("cantidad")
    nuevo_precio = request.form.get("precio")
    nuevo_proveedor = request.form.get("proveedor")
    
    
    # Verifica si se proporcionó una nueva imagen
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        # Procesamiento de la imagen
        nombre_imagen = secure_filename(imagen.filename) #Chequea el nombre del archivo de la imagen, asegurándose de que sea seguro para guardar en el sistema de archivos
        nombre_base, extension = os.path.splitext(nombre_imagen) #Separa el nombre del archivo de su extensión.
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}" #Genera un nuevo nombre para la imagen usando un timestamp, para evitar sobreescrituras y conflictos de nombres.

        # Guardar la imagen en el servidor
        imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))
        
        # Busco el producto guardado
        producto = pedidos.consultar_producto(codigo)
        if producto: # Si existe el producto...
            imagen_vieja = producto["imagen_url"]
            # Armo la ruta a la imagen
            ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

            # Y si existe la borro.
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)
    
    else:
        # Si no se proporciona una nueva imagen, simplemente usa la imagen existente del producto
        producto = pedidos.consultar_producto(codigo)
        if producto:
            nombre_imagen = producto["imagen_url"]


    # Se llama al método modificar_producto pasando el codigo del producto y los nuevos datos.
    if pedidos.modificar_producto(codigo, nueva_descripcion, nueva_cantidad, nuevo_precio, nombre_imagen, nuevo_proveedor):
        
        #Si la actualización es exitosa, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 200 (OK).
        return jsonify({"mensaje": "Producto modificado"}), 200
    else:
        #Si el producto no se encuentra (por ejemplo, si no hay ningún producto con el código dado), se devuelve un mensaje de error con un código de estado HTTP 404 (No Encontrado).
        return jsonify({"mensaje": "Producto no encontrado"}), 404
#--------------------------------------------------------------------
# Eliminar un producto según su código
#--------------------------------------------------------------------
@app.route("/productos/<int:codigo>", methods=["DELETE"])
#La ruta Flask /productos/<int:codigo> con el método HTTP DELETE está diseñada para eliminar un producto específico de la base de datos, utilizando su código como identificador.
#La función eliminar_producto se asocia con esta URL y es llamada cuando se realiza una solicitud DELETE a /productos/ seguido de un número (el código del producto).
def eliminar_producto(codigo):
    # Busco el producto en la base de datos
    producto = pedidos.consultar_producto(codigo)
    if producto: # Si el producto existe, verifica si hay una imagen asociada en el servidor.
        imagen_vieja = producto["imagen_url"]
        # Armo la ruta a la imagen
        ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

        # Y si existe, la elimina del sistema de archivos.
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

        # Luego, elimina el producto del catálogo
        if pedidos.eliminar_producto(codigo):
            #Si el producto se elimina correctamente, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 200 (OK).
            return jsonify({"mensaje": "Producto eliminado"}), 200
        else:
            #Si ocurre un error durante la eliminación (por ejemplo, si el producto no se puede eliminar de la base de datos por alguna razón), se devuelve un mensaje de error con un código de estado HTTP 500 (Error Interno del Servidor).
            return jsonify({"mensaje": "Error al eliminar el producto"}), 500
    else:
        #Si el producto no se encuentra (por ejemplo, si no existe un producto con el codigo proporcionado), se devuelve un mensaje de error con un código de estado HTTP 404 (No Encontrado). 
        return jsonify({"mensaje": "Producto no encontrado"}), 404

#--------------------------------------------------------------------

#--------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)