CREATE USER nodo3_replica IDENTIFIED BY password123;
GRANT CONNECT, RESOURCE TO nodo3_replica;
GRANT CREATE SESSION TO nodo3_replica;

CREATE TABLE sucursal (
    idsucursal      VARCHAR2(5),
    nombresucursal  VARCHAR2(15),
    ciudadsucursal  VARCHAR2(15),
    activos         NUMBER,
    region          VARCHAR2(2),
    PRIMARY KEY(idsucursal)
);

-- Crear tabla prestamo
CREATE TABLE prestamo (
    noprestamo  VARCHAR2(15),
    idsucursal  VARCHAR2(5),
    cantidad    NUMBER,
    PRIMARY KEY(noprestamo),
    FOREIGN KEY (idsucursal) REFERENCES sucursal(idsucursal)
);

INSERT INTO sucursal VALUES ('S0001', 'Downtown',     'Brooklyn',    900000, 'A');
INSERT INTO sucursal VALUES ('S0002', 'Redwood',      'Palo Alto',   2100000, 'A');
INSERT INTO sucursal VALUES ('S0003', 'Perryridge',   'Horseneck',   1700000, 'A');  
INSERT INTO sucursal VALUES ('S0004', 'Mianus',       'Horseneck',   400200, 'A');
INSERT INTO sucursal VALUES ('S0005', 'Round Hill',   'Horseneck',   8000000, 'B');
INSERT INTO sucursal VALUES ('S0006', 'Pownal',       'Bennington',  400000, 'B');
INSERT INTO sucursal VALUES ('S0007', 'North Town',   'Rye',         3700000, 'B');
INSERT INTO sucursal VALUES ('S0008', 'Brighton',     'Brooklyn',    7000000, 'B');
INSERT INTO sucursal VALUES ('S0009', 'Central',      'Rye',         400280, 'B');

INSERT INTO prestamo VALUES ('L-17', 'S0001', 1000);
INSERT INTO prestamo VALUES ('L-23', 'S0002', 2000);
INSERT INTO prestamo VALUES ('L-15', 'S0003', 1500);
INSERT INTO prestamo VALUES ('L-14', 'S0001', 1500);
INSERT INTO prestamo VALUES ('L-93', 'S0004', 500);
INSERT INTO prestamo VALUES ('L-11', 'S0005', 900);
INSERT INTO prestamo VALUES ('L-16', 'S0003', 1300);
INSERT INTO prestamo VALUES ('L-20', 'S0007', 7500);
INSERT INTO prestamo VALUES ('L-21', 'S0009', 570);