CREATE USER nodo1_regionA IDENTIFIED BY password123;
GRANT CONNECT, RESOURCE TO nodo1_regionA;
GRANT CREATE SESSION TO nodo1_regionA;


CREATE TABLE sucursal (
    idsucursal VARCHAR2(5) PRIMARY KEY,
    nombresucursal VARCHAR2(15),
    ciudadsucursal VARCHAR2(15),
    activos NUMBER,
    region VARCHAR2(2)
);

CREATE TABLE prestamo (
    noprestamo VARCHAR2(15) PRIMARY KEY,
    idsucursal VARCHAR2(5),
    cantidad NUMBER,
    FOREIGN KEY (idsucursal) REFERENCES sucursal(idsucursal)
);

-- Insertar solo datos de región A
INSERT INTO sucursal VALUES ('S0001', 'Downtown', 'Brooklyn', 900000, 'A');
INSERT INTO sucursal VALUES ('S0002', 'Redwood', 'Palo Alto', 2100000, 'A');
INSERT INTO sucursal VALUES ('S0003', 'Perryridge', 'Horseneck', 1700000, 'A');
INSERT INTO sucursal VALUES ('S0004', 'Mianus', 'Horseneck', 400200, 'A');

INSERT INTO prestamo VALUES ('L-17', 'S0001', 1000);
INSERT INTO prestamo VALUES ('L-23', 'S0002', 2000);
INSERT INTO prestamo VALUES ('L-15', 'S0003', 1500);
INSERT INTO prestamo VALUES ('L-14', 'S0001', 1500);
INSERT INTO prestamo VALUES ('L-93', 'S0004', 500);
INSERT INTO prestamo VALUES ('L-16', 'S0003', 1300);