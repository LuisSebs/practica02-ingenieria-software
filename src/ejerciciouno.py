import mysql.connector
from mysql.connector import errorcode
import imports.tablas as t
from imports.inserciones import lista_inserciones

DB_NAME = "ejerciciouno"

TABLAS = {}

TABLAS['cliente'] = (t.TABLA_CLIENTE)
TABLAS['producto'] = (t.TABLA_PRODUCTO)
TABLAS['proveedor'] = (t.TABLA_PROVEEDOR)
TABLAS['pedido'] = (t.TABLA_PEDIDO)

def crear_conexion():
    # Conexion base de datos
    return mysql.connector.connect(host="localhost",user='root',password="root")
    
def crear_basededatos():

    cnx = crear_conexion()
    cursor = cnx.cursor()
    connect = True

    try:
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failded creating database: {}".format(err))
        exit(1)
    
    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            crear_basededatos(cursor)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

    
    for table_name in TABLAS:
        table_description = TABLAS[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            if connect:
                cursor.execute(table_description)
                cursor.close()
                cnx.close()
                connect = False
            else:
                cnx = crear_conexion()
                cursor = cnx.cursor()
                cursor.execute("USE {}".format(DB_NAME))
                cnx.database = DB_NAME
                cursor.execute(table_description)
                cursor.close()
                cnx.close()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

def inserts():
    cnx = crear_conexion()
    cursor = cnx.cursor()
    cursor.execute("USE {}".format(DB_NAME))
    cnx.database = DB_NAME
    for insercion in lista_inserciones:
        sentencia = insercion.get('sentencia')
        valores = insercion.get('valores')
        cursor.execute(sentencia,valores)
        print("Insertando en tabla: OK")
    cnx.commit()
    cursor.close()
    cnx.close()

def consulta1(cursor):

    sql = "SELECT * FROM Cliente WHERE estado = 'Durango';"
    cursor.execute(sql)
    resultados = cursor.fetchall()
    for fila in resultados:
        print(resultados)

def consulta2(cursor):

    sql = "SELECT * FROM Proveedor WHERE email LIKE '%@gmail%';"
    cursor.execute(sql)
    resultados = cursor.fetchall()
    for fila in resultados:
        print(fila)

def consulta3(cursor):

    sql = "SELECT * FROM Producto WHERE precio > 100;"
    cursor.execute(sql)
    resultados = cursor.fetchall()
    for fila in resultados:
        print(fila)

def consulta4(cursor):

    sql = "SELECT * FROM Producto WHERE precio BETWEEN 15 AND 50;"
    cursor.execute(sql)
    resultados = cursor.fetchall()
    for fila in resultados:
        print(fila)

def consulta5(cursor):

    sql = "SELECT * FROM ejerciciouno.Pedido WHERE total > 200 AND cantidad >= 10;"
    cursor.execute(sql)
    resultados = cursor.fetchall()
    for fila in resultados:
        print(fila)

def consulta6(cursor):
    # obtener a los proveedores con cede en Ciudad de Mexico o Monterrey
    sql = "SELECT * FROM Proveedor WHERE ciudad = 'Ciudad de Mexico' OR ciudad = 'Monterrey';"
    cursor.execute(sql)
    resultados = cursor.fetchall()
    for fila in resultados:
        print(fila)

def update(cursor,cnx):
    # actualizar el precio en 0 de los productos con el id 1,2,3,4

    print("UPDATE: actualizar el precio en 0 de los productos con el id 1,2,3,4\n")

    # Mostramos los productos a actualizar
    print("\n\t --ANTES DE ACTUALIZAR-- \n")
    sql = "SELECT * FROM Producto WHERE id IN (1,2,3,4);"
    cursor.execute(sql)
    resultados = cursor.fetchall()
    for fila in resultados:
        print(fila)

    sql = "UPDATE Producto SET precio = 0 WHERE id IN (1,2,3,4);"
    cursor.execute(sql)
    cnx.commit()

    # Volvemos a mostrar los resultados
    print("\n\t --DESPUES DE ACTUALIZAR--\n")
    sql = "SELECT * FROM Producto WHERE id IN (1,2,3,4);"
    cursor.execute(sql)
    resultados = cursor.fetchall()
    for fila in resultados:
        print(fila)
    
def delete(cursor,cnx):

    print("DELETE: Elimina los pedidos cuyo productos no tiene existencia\n")

    # Productos a eliminar
    print("\n\t --PEDIDOS ELIMINAR--\n")
    sql = "SELECT * FROM Pedido INNER JOIN Producto ON Pedido.producto = Producto.id WHERE Producto.existencia = 0"
    cursor.execute(sql)
    resultados = cursor.fetchall()
    for fila in resultados:
        print(fila)

    print()
    # Elimina los pedidos cuyo productos no tiene existencia
    sql = "DELETE FROM Pedido WHERE producto IN (SELECT id FROM Producto WHERE existencia = FALSE);"
    cursor.execute(sql)
    cnx.commit()

     # Productos a eliminar
    print("\n\t --BUSCAMOS LOS PEDIDOS ELIMINADOS--\n")
    sql = "SELECT * FROM Pedido INNER JOIN Producto ON Pedido.producto = Producto.id WHERE Producto.existencia = 0"
    cursor.execute(sql)
    resultados = cursor.fetchall()
    for fila in resultados:
        print(fila)

def existe_database():
    cnx = crear_conexion()
    cursor = cnx.cursor()
    cursor.execute("SHOW DATABASES")
    for base in cursor:
        if DB_NAME in base:
            return True
    return False

if __name__ == "__main__":

    menu = """
[1] Crear 
[2] Read
[3] Update
[4] Delete
[0] Salir
"""
    # Verificamos si la base de datos ya existe
    database_creada = existe_database()

    while True:
        
        # Conexion
        cnx = None
        # Cursor
        cursor = None

        # Inizialicamos la conexion y el cursor
        if database_creada:
            cnx = crear_conexion()
            cursor = cnx.cursor()
            cursor.execute("USE {}".format(DB_NAME)) 

        # Mostramos el menu
        print(menu)

        # Opcion usuario
        op = input("Elige una opcion: ")

        if op == '1': # Create
            if not database_creada:
                # Creamos base de datos
                crear_basededatos()
                # Poblamos
                inserts()
                database_creada = True
            else:
                print("Ya existe la base de datos")
        elif op == '2': # Read
            if database_creada:
                # Submenu consultas
                consultas = "[1] consulta1\n[2] consulta2\n[3] consulta3\n[4] consulta4\n[5] consulta5\n[6] consulta6\n[0] Regresar"

                while True:
                    print(consultas)
                    op = input("Elige una opcion: ")
                    if op == '1': # Consulta1
                        consulta1(cursor)
                        print()
                    elif op == '2': # Consulta2
                        consulta2(cursor)
                        print()
                    elif op == '3': # Consulta3
                        consulta3(cursor)
                        print()
                    elif op == '4': # Consulta4
                        consulta4(cursor)
                        print()
                    elif op == '5': # Consulta5
                        consulta5(cursor)
                        print()
                    elif op == '6': # Consulta6
                        consulta6(cursor)
                        print()
                    elif op == '0': # Regresar
                        break
                    else:
                        print("Elige una opcion valida")
            else:
                print("Primero crea la base de datos por favor") 
        elif op == '3': # Update
            if database_creada:
                update(cursor,cnx)
                print()
            else:
                print("Primero crea la base de datos por favor") 
        elif op == '4': # Delete
            if database_creada:
                delete(cursor,cnx)   
                print()
            else:
                print("Primero crea la base de datos por favor") 
        elif op == '0':
            cursor.close()
            cnx.close()
            exit(0)
        else:
            print("Elige una opcion valida")





