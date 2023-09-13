conexion = mysql.connector.connect(
host="localhost",
user="root",
password="root",
database="ejerciciouno"
)

#cursor.execute("CREATE TABLE IF NOT EXISTS Cliente( ID INTEGER, Nombre VARCHAR(255) NOT NULL, Domicilio VARCHAR(255) NOT NULL, Ciudad VARCHAR(255) NOT NULL, Estado VARCHAR(255) NOT NULL, CodigoPostal VARCHAR(5) NOT NULL, Email VARCHAR(255) NOT NULL); ALTER TABLE Cliente ADD CONSTRAINT pk_Cliente PRIMARY KEY (ID);")
cursor.execute(s.TABLA_CLIENTE)
cursor.execute(s.TABLA_PRODUCTO)



    


