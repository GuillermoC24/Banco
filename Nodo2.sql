CREATE DATABASE nodo2_regionB;
USE nodo2_regionB;


CREATE TABLE sucursal (
    idsucursal VARCHAR(5) PRIMARY KEY,
    nombresucursal VARCHAR(15),
    ciudadsucursal VARCHAR(15),
    activos DECIMAL(10,2),
    region VARCHAR(2)
);

CREATE TABLE prestamo (
    noprestamo VARCHAR(15) PRIMARY KEY,
    idsucursal VARCHAR(5),
    cantidad DECIMAL(10,2),
    FOREIGN KEY (idsucursal) REFERENCES sucursal(idsucursal)
);

-- Insertar solo datos de región B
INSERT INTO sucursal VALUES ('S0005', 'Round Hill', 'Horseneck', 8000000, 'B');
INSERT INTO sucursal VALUES ('S0006', 'Pownal', 'Bennington', 400000, 'B');
INSERT INTO sucursal VALUES ('S0007', 'North Town', 'Rye', 3700000, 'B');
INSERT INTO sucursal VALUES ('S0008', 'Brighton', 'Brooklyn', 7000000, 'B');
INSERT INTO sucursal VALUES ('S0009', 'Central', 'Rye', 400280, 'B');

INSERT INTO prestamo VALUES ('L-11', 'S0005', 900);
INSERT INTO prestamo VALUES ('L-20', 'S0007', 7500);
INSERT INTO prestamo VALUES ('L-21', 'S0009', 570);