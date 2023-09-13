import re

# Lista de inserciones
lista_inserciones = list()

ruta_dml = "../sql/DML.sql"
archivo = open(ruta_dml)
lineas = archivo.readlines()

regex_insert = r"INSERT INTO [A-Za-z]+ [(][A-Za-z,\s]+[)] VALUES "
regex_values = r"VALUES [(][0-9A-Za-zÁ-Źá-ź-@.\u00f1\u00d1',\s]+[);]+"
regex_placeholder = r"('[0-9\sa-zA-Zá-źÁ-Ź-@.\u00f1\u00d1,\s]+')|([0-9]+)"
regex_ubicar_valores = r"([0-9]+)|('[0-9á-źÁ-Źa-zA-z\u00f1\u00d1,\s@.-]+')"

for linea in lineas:
    # Extraemos la sentencia insert y los campos
    inserta_en = None
    campos = list()

    sentencia_insert = re.search(regex_insert,linea) # Sentencia INSERT INTO tabla VALUES (...)

    if sentencia_insert:
        # Obtenemos los campos
        sentencia_campos = re.search("[()][A-za-z,\s]+[)]",sentencia_insert.group()) 
        sentencia_campos = sentencia_campos.group() 
        sentencia_campos = sentencia_campos[1:len(sentencia_campos)-1] 
        campos = sentencia_campos.split(", ")
        
        # Extraemos la sentencia VALUES
        sentencia_values = re.search(regex_values,linea) # Extraemos la sentencia VALUES con los valores
        sentencia_values = sentencia_values.group().replace("VALUES ","") # Eliminamos el VALUES 

        # Creamos la sentencia de los placeholders (%s,...,%s)
        placeholder = re.sub(regex_placeholder,'%s',sentencia_values)

        # Sentencia insert con los placeholders
        insert_into_table = sentencia_insert.group()+""+placeholder

        # Extraemos los valores
        valores = sentencia_values[1:len(sentencia_values)-2] # Eliminamos los parentesis de los extremos y el punto y coma
        valores = re.findall(regex_ubicar_valores,valores)
        valores = [v[1] if len(v[0]) == 0 else v[0] for v in valores]
        valores = [v.replace("'",'')for v in valores] # Eliminamos las comillas simples de los valores()

        valores_casteados = list()

        if len(campos) == len(valores):
            n = len(campos)
            for i in range(n):
                # Si el campo es codigo postal entonces no lo casteamos
                if campos[i] == "CodigoPostal":
                    valores_casteados.append(valores[i])
                else:
                    # Intentamos castear el valor a entero
                    v = valores[i]
                    try:
                        v = int(v)
                    except:
                        pass
                    valores_casteados.append(v)
        
        # Convertimos la lista de valores a una tupla
        values = tuple(valores_casteados)

        # Agregamos la sentencia insert y los valores
        lista_inserciones.append({
            'sentencia':insert_into_table,
            'valores':values
        })  