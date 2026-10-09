-- ===== PostgreSQL 16: estructura + datos =====
DROP TABLE IF EXISTS detalle_pedidos;
DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS categorias;

CREATE TABLE categorias (
  id_categoria SERIAL PRIMARY KEY,
  nombre VARCHAR(60) NOT NULL UNIQUE
);

CREATE TABLE productos (
  id_producto SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  precio NUMERIC(10,2) NOT NULL CHECK (precio >= 0),
  stock INTEGER NOT NULL DEFAULT 0,
  id_categoria INTEGER NOT NULL REFERENCES categorias(id_categoria)
);

CREATE TABLE clientes (
  id_cliente SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  correo VARCHAR(120) NOT NULL UNIQUE,
  ciudad VARCHAR(60)
);

CREATE TABLE pedidos (
  id_pedido SERIAL PRIMARY KEY,
  id_cliente INTEGER NOT NULL REFERENCES clientes(id_cliente),
  fecha DATE NOT NULL,
  estado VARCHAR(20) NOT NULL DEFAULT 'pendiente'
);

CREATE TABLE detalle_pedidos (
  id_detalle SERIAL PRIMARY KEY,
  id_pedido INTEGER NOT NULL REFERENCES pedidos(id_pedido),
  id_producto INTEGER NOT NULL REFERENCES productos(id_producto),
  cantidad INTEGER NOT NULL CHECK (cantidad > 0),
  precio_unitario NUMERIC(10,2) NOT NULL
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
