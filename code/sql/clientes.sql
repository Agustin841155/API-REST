Drop TABLE IF EXISTS clientes;
CREATE TABLE clientes(
    id_cliente integer PRIMARY KEY AUTOINCREMENT,
    nombre varchar(50) NOT NULL,
    email varchar(50) NOT NULL
);
INSERT INTO clientes(nombre, email) VALUES ('Dejah', 'dejah@gmail.com');
INSERT INTO clientes(nombre, email) VALUES ('John', 'john@gmail.com');
INSERT INTO clientes(nombre, email) VALUES ('Carthoris', 'carthoris@gmail.com');

.headers ON

SELECT * FROM clientes;