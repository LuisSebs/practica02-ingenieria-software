# Práctica 02: Ingenieria de Software

## Autor: Arrieta Mancera Luis Sebastian

Para esta práctica se crearon dos archivos con el nombre de `ejerciciouno.py`,  `ejercicio2.py` para lo cual antes de correrlos hay que tener en cuenta las siguientes consideraciones:

- Es necesario crear una base de datos
llamada `ejerciciodos` en mysql para `ejerciciodos.py`. De preferencia solo correr el archivo una sola vez o puede tener errores.

- Para el `ejerciciouno.py` se puede correr las veces que sea puesto que desde ese archivo se creo la base de datos y tiene procedimientos para no tronar en caso de que ya se haya creado o no la base de datos.

- En caso de que no funcione alguno de los archivos, favor de correr el entorno virtual con los comandos `$ cd myenv` y `source ./bin/activate`.

- Favor de seguir el orden del menu (create, read, update, delete) para que los ejemplos se vean lo mejor posible, a pesar de que sea robusto.

- Se tiene archivo `DDL.sql` para ambos esquemas y en cada carpeta dentro de `./sql` esta su correspondiente `DQL.sql` para visualizar las consultas.

- Se implementaron **expresiones regulares** para poder extraer las inserciones diractamente del archivo `DML.sql` que cuenta con cierta cantidad de robustes en caso de que se quieran agregar más datos o modificarlos (siguiendo la estructura de las tablas).

## Para correr los programas:

Favor de posicionarse en la carpeta `./src` para ejecutar los programas

```cmd
$ python3 ejerciciouno.py

$ python3 ejerciciodos.py
```

Cualquier problema con la ejecución de los programas favor de contactarme y gracias...

![github octocat](https://media.giphy.com/media/cDZJ17fbzWVle68VCB/giphy.gif)

