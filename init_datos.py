

import cx_Oracle
import mysql.connector

def inicializar_oracle_nodo1():
    """Inicializa datos en Oracle Nodo 1 - Región A"""
    try:
        conn = cx_Oracle.connect('nodo1_regionA/password123@localhost:1521/XEPDB1')
        cursor = conn.cursor()
        
        # Limpiar tablas
        cursor.execute("DELETE FROM prestamo")
        cursor.execute("DELETE FROM sucursal")
        
        # Datos región A
        sucursales_a = [
            ('S0001', 'Downtown', 'Brooklyn', 900000, 'A'),
            ('S0002', 'Redwood', 'Palo Alto', 2100000, 'A'),
            ('S0003', 'Perryridge', 'Horseneck', 1700000, 'A'),
            ('S0004', 'Mianus', 'Horseneck', 400200, 'A')
        ]
        
        prestamos_a = [
            ('L-17', 'S0001', 1000),
            ('L-23', 'S0002', 2000),
            ('L-15', 'S0003', 1500),
            ('L-14', 'S0001', 1500),
            ('L-93', 'S0004', 500),
            ('L-16', 'S0003', 1300)
        ]
        
        # Insertar sucursales
        for sucursal in sucursales_a:
            cursor.execute("INSERT INTO sucursal VALUES (:1, :2, :3, :4, :5)", sucursal)
        
        # Insertar préstamos
        for prestamo in prestamos_a:
            cursor.execute("INSERT INTO prestamo VALUES (:1, :2, :3)", prestamo)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✓ Oracle Nodo 1 (Región A) inicializado correctamente")
        
    except Exception as e:
        print(f"Error inicializando Oracle Nodo 1: {e}")

def inicializar_mysql_nodo2():
    """Inicializa datos en MySQL Nodo 2 - Región B"""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='nodo2_regionB',
            user='root',
            password='admin'
        )
        cursor = conn.cursor()
        
        # Limpiar tablas
        cursor.execute("DELETE FROM prestamo")
        cursor.execute("DELETE FROM sucursal")
        
        # Datos región B
        sucursales_b = [
            ('S0005', 'Round Hill', 'Horseneck', 8000000, 'B'),
            ('S0006', 'Pownal', 'Bennington', 400000, 'B'),
            ('S0007', 'North Town', 'Rye', 3700000, 'B'),
            ('S0008', 'Brighton', 'Brooklyn', 7000000, 'B'),
            ('S0009', 'Central', 'Rye', 400280, 'B')
        ]
        
        prestamos_b = [
            ('L-11', 'S0005', 900),
            ('L-20', 'S0007', 7500),
            ('L-21', 'S0009', 570)
        ]
        
        # Insertar sucursales
        for sucursal in sucursales_b:
            cursor.execute("INSERT INTO sucursal VALUES (%s, %s, %s, %s, %s)", sucursal)
        
        # Insertar préstamos
        for prestamo in prestamos_b:
            cursor.execute("INSERT INTO prestamo VALUES (%s, %s, %s)", prestamo)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✓ MySQL Nodo 2 (Región B) inicializado correctamente")
        
    except Exception as e:
        print(f"Error inicializando MySQL Nodo 2: {e}")

def inicializar_oracle_replica():
    """Inicializa datos completos en Oracle Nodo 3 - Réplica"""
    try:
        conn = cx_Oracle.connect('nodo3_replica/password123@localhost:1521/XEPDB1')
        cursor = conn.cursor()
        
        # Limpiar tablas
        cursor.execute("DELETE FROM prestamo")
        cursor.execute("DELETE FROM sucursal")
        
        # Todos los datos (A + B)
        todas_sucursales = [
            ('S0001', 'Downtown', 'Brooklyn', 900000, 'A'),
            ('S0002', 'Redwood', 'Palo Alto', 2100000, 'A'),
            ('S0003', 'Perryridge', 'Horseneck', 1700000, 'A'),
            ('S0004', 'Mianus', 'Horseneck', 400200, 'A'),
            ('S0005', 'Round Hill', 'Horseneck', 8000000, 'B'),
            ('S0006', 'Pownal', 'Bennington', 400000, 'B'),
            ('S0007', 'North Town', 'Rye', 3700000, 'B'),
            ('S0008', 'Brighton', 'Brooklyn', 7000000, 'B'),
            ('S0009', 'Central', 'Rye', 400280, 'B')
        ]
        
        todos_prestamos = [
            ('L-17', 'S0001', 1000),
            ('L-23', 'S0002', 2000),
            ('L-15', 'S0003', 1500),
            ('L-14', 'S0001', 1500),
            ('L-93', 'S0004', 500),
            ('L-16', 'S0003', 1300),
            ('L-11', 'S0005', 900),
            ('L-20', 'S0007', 7500),
            ('L-21', 'S0009', 570)
        ]
        
        # Insertar todos los datos
        for sucursal in todas_sucursales:
            cursor.execute("INSERT INTO sucursal VALUES (:1, :2, :3, :4, :5)", sucursal)
        
        for prestamo in todos_prestamos:
            cursor.execute("INSERT INTO prestamo VALUES (:1, :2, :3)", prestamo)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✓ Oracle Nodo 3 (Réplica) inicializado correctamente")
        
    except Exception as e:
        print(f"Error inicializando Oracle Nodo 3: {e}")

def main():
    """Función principal para inicializar todos los nodos"""
    print("=== INICIALIZANDO BASE DE DATOS DISTRIBUIDA ===\n")
    
    print("1. Inicializando Oracle Nodo 1 (Región A)...")
    inicializar_oracle_nodo1()
    
    print("\n2. Inicializando MySQL Nodo 2 (Región B)...")
    inicializar_mysql_nodo2()
    
    print("\n3. Inicializando Oracle Nodo 3 (Réplica)...")
    inicializar_oracle_replica()
    
    print("\n¡Inicialización completa!")
    print("Puede ejecutar la aplicación principal ahora.")

if __name__ == "__main__":
    main()