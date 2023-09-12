import re

# (1, 'Laura', '8234 Rigney Drive', 'Reynosa', 'México', '19486', 'laura@gmail.com');

src = "../sql/ejercicio1/DML.sql"

inserts = []
datas = []

sql_file = open(src)
lines = sql_file.readlines()

for line in lines:

    fields = {}

    regex_insert = r"INSERT INTO [A-Za-z]+ [(][A-Za-z,\s]+[)] VALUES "
    regex_values = r"VALUES [(][0-9A-Za-zÁ-Źá-ź-@.\u00f1\u00d1',\s]+[);]+"
    regex_placeholder = r"('[0-9\sa-zA-Zá-źÁ-Ź-@.\u00f1\u00d1,\s]+')|([0-9]+)"

    insert = re.search(regex_insert,line)

    f = None
    if insert:
        f = re.search("[()][A-za-z,\s]+[)]",insert.group())
        if f:
            f = f.group()
            # Removemos parentesis ()
            f = f[1:len(f)-1]
            # separamos los campos
            f = f.split(", ")


    value = re.search(regex_values,line)

    if value:
        # Place holders
        value = value.group().replace("VALUES ","")
        placeholder = re.sub(regex_placeholder,'%s',value)    
        inserts.append(insert.group()+""+placeholder)

        # Values without (
        value = value[1:]
        # Value without )
        value = value.replace(");",'')
        # Otra regex para separar los valores
        value = re.findall("([0-9]+)|('[0-9á-źÁ-Źa-zA-z\u00f1\u00d1,\s@.-]+')",value)
        if value:

            value = [ v[1] if len(v[0]) == 0 else v[0] for v in value]
        
        # Values string list without ''
        value = [v.replace("'",'') for v in value]

        # Valores finales
        cast_values = list()

        
        # Eliminamos comillas simples de los numeros
        if f:
            if len(f) == len(value):
                for i in range(len(f)):
                    # A menos que sea un codigo postal (nos basamos en el campo)
                    if f[i] == 'CodigoPostal':
                        cast_values.append(value[i])
                    else:
                        v = value[i]
                        try:
                            v = int(v)
                        except ValueError:
                            pass
                        cast_values.append(v)
            
        
        # Tupla base
        data = tuple(cast_values)
        datas.append(data)

        

        
        




                
            

        



        
    


        
        





    