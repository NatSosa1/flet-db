-- ===== MySQL 8: estructura + datos =====
CREATE DATABASE IF NOT EXISTS tienda CHARACTER SET utf8mb4;
USE tienda;

DROP TABLE IF EXISTS detalle_pedidos;
DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS categorias;

CREATE TABLE categorias (
  id_categoria INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(60) NOT NULL UNIQUE
);

CREATE TABLE productos (
  id_producto INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  precio DECIMAL(10,2) NOT NULL CHECK (precio >= 0),
  stock INT NOT NULL DEFAULT 0,
  id_categoria INT NOT NULL,
  FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);

CREATE TABLE clientes (
  id_cliente INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  correo VARCHAR(120) NOT NULL UNIQUE,
  ciudad VARCHAR(60)
);

CREATE TABLE pedidos (
  id_pedido INT AUTO_INCREMENT PRIMARY KEY,
  id_cliente INT NOT NULL,
  fecha DATE NOT NULL,
  estado VARCHAR(20) NOT NULL DEFAULT 'pendiente',
  FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

CREATE TABLE detalle_pedidos (
  id_detalle INT AUTO_INCREMENT PRIMARY KEY,
  id_pedido INT NOT NULL,
  id_producto INT NOT NULL,
  cantidad INT NOT NULL CHECK (cantidad > 0),
  precio_unitario DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido),
  FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

INSERT INTO categorias (nombre) VALUES ('Electrónica'),('Papelería'),('Accesorios');

INSERT INTO productos (nombre, precio, stock, id_categoria) VALUES
('Audífonos Bluetooth', 499.00, 25, 1),
('Teclado mecánico', 899.50, 12, 1),
('Cuaderno profesional', 45.00, 120, 2),
('Set de plumas', 79.90, 60, 2),
('Mochila para laptop', 650.00, 18, 3),
('Soporte para celular', 120.00, 40, 3);

INSERT INTO clientes (nombre, correo, ciudad) VALUES
('Ana Torres', 'ana@correo.com', 'Toluca'),
('Luis Pérez', 'luis@correo.com', 'Monterrey'),
('María López', 'maria@correo.com', 'CDMX'),
('Carlos Ruiz', 'carlos@correo.com', 'Toluca');

INSERT INTO pedidos (id_cliente, fecha, estado) VALUES
(1, '2026-09-01', 'entregado'),
(2, '2026-09-05', 'enviado'),
(3, '2026-09-10', 'pendiente'),
(1, '2026-09-20', 'pendiente');

INSERT INTO detalle_pedidos (id_pedido, id_producto, cantidad, precio_unitario) VALUES
(1, 1, 1, 499.00),
(1, 3, 3, 45.00),
(2, 2, 1, 899.50),
(3, 5, 1, 650.00),
(3, 6, 2, 120.00),
(4, 4, 5, 79.90);
