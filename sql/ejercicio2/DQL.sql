-- Consulta 1 
SELECT * FROM Cliente WHERE nombre LIKE "E%";

-- Consulta 2
SELECT * FROM Proveedor WHERE email LIKE "%a%@%";

-- Consulta 3
SELECT * FROM Producto WHERE existencia = true;

-- Consulta 4
SELECT * FROM Producto WHERE marca LIKE "D%";

-- Consulta 5
SELECT * FROM Pedido WHERE fecha BETWEEN '2023-01-24' AND '2023-04-24';

-- Consulta 6
-- obtener la cantidad de los proveedores cuyo codigo postal comienza con 6 o 9
SELECT COUNT(id) AS "cantidad" FROM Proveedor WHERE codigopostal LIKE "6%" OR codigopostal LIKE "9%";

-- UPDATE
-- subir los precios de los productos con id 1,2,3 y 4 en un 2%.
-- precios antes del update:
-- 1 = 153
-- 2 = 156
-- 3 = 55
-- 4 = 59
UPDATE Producto SET precio = precio + precio * 0.02 WHERE id IN (1,2,3,4);
-- Mostramos los registros modificados
SELECT * FROM Producto WHERE id IN (1,2,3,4);

-- DELETE
-- eliminar a los clientes con id 1,2,3,4 y 5
DELETE FROM Cliente WHERE id IN (1,2,3,4,5);