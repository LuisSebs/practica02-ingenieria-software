-- Consulta 1
SELECT * FROM Cliente WHERE estado = "Durango";

-- Consulta 2
SELECT * FROM Proveedor WHERE email LIKE "%@gmail%";

-- Consulta 3
SELECT * FROM Producto WHERE precio > 100;

-- Consulta 4
SELECT * FROM Producto WHERE precio BETWEEN 15 AND 50;

-- Consulta 5
SELECT * FROM Pedido WHERE total > 200 AND cantidad >= 10;

-- Consulta 6
-- obtener a los proveedores con cede en Ciudad de Mexico o Monterrey
SELECT * FROM Proveedor WHERE ciudad = "Ciudad de Mexico" OR ciudad = "Monterrey";

-- UPDATE
-- actualizar el precio en 0 de los productos con el id 1,2,3,4
UPDATE Producto SET precio = 0 WHERE id IN (1,2,3,4);
-- Mostramos los productos modificados
SELECT * FROM Producto ORDER BY precio;

-- DELETE
-- Elimina los pedidos cuyo productos no tiene existencia
DELETE FROM Pedido WHERE producto IN (SELECT id FROM Producto WHERE existencia = FALSE);

