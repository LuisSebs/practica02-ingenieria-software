from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from sqlalchemy import or_, func
import mysql.connector
from imports.inserciones import lista_inserciones
import re

DB_NAME = 'ejerciciodos'

# Instancia
engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/{}'.format(DB_NAME))

# Base declarativa
Base = declarative_base()

# Tabla Cliente:
class Cliente(Base):
    __tablename__ = 'Cliente'
    id = Column(Integer, primary_key = True)
    nombre = Column(String(255), nullable = False)
    domicilio = Column(String(255), nullable = False)
    ciudad = Column(String(255), nullable = False)
    estado = Column(String(255), nullable = False)
    codigo_postal = Column(String(255), nullable = False)
    email = Column(String(255), nullable = False)

# Tabla Producto
class Producto(Base):
    __tablename__ = 'Producto'
    id = Column(Integer, primary_key = True)
    descripcion = Column(String(255), nullable = False)
    precio = Column(Integer, nullable = False)
    marca = Column(String(255), nullable = False)
    existencia = Column(Boolean, nullable = False)

# Tabla Proveedores
class Proveedor(Base):
    __tablename__ = 'Proveedor'
    id = Column(Integer, primary_key = True)
    empresa = Column(String(255), nullable = False)
    nombre_contacto = Column(String(255), nullable = False)
    direccion = Column(String(255), nullable = False)
    ciudad = Column(String(255), nullable = False)
    estado = Column(String(255), nullable = False)
    codigo_postal = Column(String(5), nullable = False)
    email = Column(String(255), nullable = False)

# Tabla Pedido
class Pedido(Base):
    __tablename__ = 'Pedido'
    id = Column(Integer, primary_key = True)
    vendedor = Column(String(255), nullable = False)
    fecha = Column(DateTime, nullable = False)
    producto = Column(Integer, nullable = False)
    cantidad = Column(Integer, nullable = False)
    precio = Column(Integer, nullable = False)
    total = Column(Integer, nullable = False)

def crear_tablas():
    # Creamos las tablas
    Base.metadata.create_all(engine)

def poblar_tablas(session):

    for insercion in lista_inserciones:
        sentencia = insercion.get('sentencia')
        valores = insercion.get('valores')
        # Si la sentencia contiene la palabra Cliente
        if re.search("INSERT INTO Cliente",sentencia):
            nuevo_cliente = Cliente(
                id = valores[0],
                nombre = valores[1],
                domicilio = valores[2],
                ciudad = valores[3],
                estado = valores[4],
                codigo_postal = valores[5],
                email = valores[6]
            )
            session.add(nuevo_cliente)

        # Si la sentencia contiene la palabra Producto
        if re.search("INSERT INTO Producto",sentencia):
            nuevo_producto = Producto(
                id = valores[0],
                descripcion = valores[1],
                precio = valores[2],
                marca = valores[3],
                existencia = valores[4]
            )
            session.add(nuevo_producto)
                
        # Si la sentencia contiene la palabra Proveedor
        if re.search("INSERT INTO Proveedor",sentencia):
            nuevo_proveedor = Proveedor(
                id = valores[0],
                empresa = valores[1],
                nombre_contacto = valores[2],
                direccion = valores[3],
                ciudad = valores[4],
                estado = valores[5],
                codigo_postal = valores[6],
                email = valores[7]
            )
            session.add(nuevo_proveedor)
        
        # Si la sentencia contiene la palabra Pedido
        if re.search("INSERT INTO Pedido",sentencia):
            nuevo_pedido = Pedido(
                id = valores[0],
                vendedor = valores[1],
                fecha = valores[2],
                producto = valores[3],
                cantidad = valores[4],
                precio = valores[5],
                total = valores[6]
            )
            session.add(nuevo_pedido)

    session.commit()

def consulta1(session):
    #  todos los clientes su nombre empiece con E (al menos debe existir uno).
    resultado = session.query(Cliente).filter(Cliente.nombre.like('E%')).all()
    for cliente in resultado:
        print(cliente.id,cliente.nombre,cliente.domicilio,cliente.ciudad,cliente.estado,cliente.codigo_postal,cliente.email)

def consulta2(session):
    # los proveedores que su correo contenga al menos una letra a
    resultado = session.query(Proveedor).filter(Proveedor.email.like('%a%@%')).all()
    for proveedor in resultado:
        print(proveedor.id,proveedor.empresa,proveedor.nombre_contacto,proveedor.direccion,proveedor.ciudad,proveedor.estado,proveedor.codigo_postal,proveedor.email)

def consulta3(session):
     # los productos que tengan existencia
     resultado = session.query(Producto).filter(Producto.existencia == True).all()
     for producto in resultado:
        print(producto.id,producto.descripcion,producto.precio,producto.marca,producto.existencia)

def consulta4(session):
    # los productos que la marca empiece con D
    resultado = session.query(Producto).filter(Producto.marca.like('D%')).all()
    for producto in resultado:
        print(producto.id,producto.descripcion,producto.precio,producto.marca,producto.existencia)

def consulta5(session):
    fecha_inicio = '2023-01-24'
    fecha_fin = '2023-04-24'
    # los pedidos que la su fecha sea entre 24/01/2023 al 24/04/2023
    resultado = session.query(Pedido).filter(and_(Pedido.fecha >= fecha_inicio, Pedido.fecha <= fecha_fin)).all()
    for pedido in resultado:
        print(pedido.id,pedido.vendedor,pedido.fecha,pedido.producto,pedido.cantidad,pedido.precio,pedido.total)

def consulta6(session):
    # obtener la cantidad de los proveedores cuyo codigo postal comienza con 6 o 9
    print("obtener la cantidad de los proveedores cuyo codigo postal comienza con 6 o 9\n")
    resultado = session.query(func.count(Proveedor.id).label("cantidad")).filter(or_(Proveedor.codigo_postal.like('6%'), Proveedor.codigo_postal.like('9%'))).first()
    print(f"La cantidad es: {resultado}")

def update(session):

    # -- subir los precios de los productos con id 1,2,3 y 4 en un 2%.
    # precios antes del update:
    print("UPDATE: subir los precios de los productos con id 1,2,3 y 4 en un 2%.")
    ids_a_actualizar = [1, 2, 3, 4]
    incremento_porcentaje = 0.02

    # Obtener los productos con los IDs especificados
    productos_a_actualizar = session.query(Producto).filter(Producto.id.in_(ids_a_actualizar)).all()

    # Actualizar el precio de cada producto
    for producto in productos_a_actualizar:
        producto.precio = producto.precio + (producto.precio * incremento_porcentaje)

    # Mostramos los registros modificados
    resultado = session.query(Producto).filter(Producto.id.in_(ids_a_actualizar)).all()
    for producto in resultado:
        print(producto.id,producto.descripcion,producto.precio,producto.marca,producto.existencia)

def delete(session):
    # eliminar a los clientes con id 1,2,3,4 y 5
    print("DELETE: eliminar a los clientes con id 1,2,3,4 y 5")
    ids_a_eliminar = [1, 2, 3, 4, 5]
    # Clientes a eliminar (id's)
    clientes_a_eliminar = session.query(Cliente).filter(Cliente.id.in_(ids_a_eliminar)).all()
    # Eliminar los clientes obtenidos
    for cliente in clientes_a_eliminar:
        session.delete(cliente)
   
if __name__ == "__main__":
    
    Session = sessionmaker(bind=engine)
    session = Session()

    menu = """
[1] Crear 
[2] Read
[3] Update
[4] Delete
[0] Salir
"""

    while True:
            
            # Mostramos el menu
            print(menu)

            # Opcion usuario
            op = input("Elige una opcion: ")

            if op == '1': # Create
                    crear_tablas()
                    poblar_tablas(session)
            elif op == '2': # Read
                    # Submenu consultas
                    consultas = "[1] consulta1\n[2] consulta2\n[3] consulta3\n[4] consulta4\n[5] consulta5\n[6] consulta6\n[0] Regresar"
                    while True:
                        print(consultas)
                        op = input("Elige una opcion: ")
                        if op == '1': # Consulta1
                            consulta1(session)
                            print()
                        elif op == '2': # Consulta2
                            consulta2(session)
                            print()
                        elif op == '3': # Consulta3
                            consulta3(session)
                            print()
                        elif op == '4': # Consulta4
                            consulta4(session)
                            print()
                        elif op == '5': # Consulta5
                            consulta5(session)
                            print()
                        elif op == '6': # Consulta6
                            consulta6(session)
                            print()
                        elif op == '0': # Regresar
                            break
                        else:
                            print("Elige una opcion valida")
            elif op == '3': # Update
                    update(session)
                    print()
            elif op == '4': # Delete
                    delete(session)
                    print()
            elif op == '0':
                session.commit()
                session.close()
                exit(0)
            else:
                print("Elige una opcion valida")