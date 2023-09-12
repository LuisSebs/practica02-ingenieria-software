import mysql.connector
from mysql.connector import errorcode
import tablas as t
import inserts as i

DB_NAME = "ejerciciouno"

TABLES = {}

TABLES['cliente'] = (t.TABLA_CLIENTE)
TABLES['producto'] = (t.TABLA_PRODUCTO)
TABLES['proveedor'] = (t.TABLA_PROVEEDOR)
TABLES['pedido'] = (t.TABLA_PEDIDO)

def create_conection():
    # Conexion base de datos
    return mysql.connector.connect(host="localhost",user='root',password="root")
    
def create_database():

    cnx = create_conection()
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
            create_database(cursor)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

    
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            if connect:
                cursor.execute(table_description)
                cursor.close()
                cnx.close()
                connect = False
            else:
                cnx = create_conection()
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

    cnx = create_conection()
    cursor = cnx.cursor()
    cursor.execute("USE {}".format(DB_NAME))
    cnx.database = DB_NAME
    for j in range(len(i.inserts)):
        cursor.execute(i.inserts[j],i.datas[j])
        cnx.commit()
    
    cursor.close()
    cnx.close()
        

create_database()
inserts()