import cx_Oracle
import mysql.connector
from mysql.connector import Error
import sys

class BaseDatosDistribuida:
    def __init__(self):
        self.conexiones = {}
        self.conectar_nodos()
    
    def conectar_nodos(self):
        """Conecta a todos los nodos de la base de datos distribuida"""
        try:
            # Nodo 1 - Oracle - Región A (Nodo Principal)
            self.conexiones['nodo1_oracle_A'] = cx_Oracle.connect(
                user='nodo1_regionA',
                password='password123',
                dsn='localhost:1521/XEPDB1'  
            )
            print("✓ Conectado al Nodo 1 (Oracle - Región A)")
            
            # Nodo 2 - MySQL - Región B
            self.conexiones['nodo2_mysql_B'] = mysql.connector.connect(
                host='localhost',
                database='nodo2_regionB',
                user='root',  
                password='admin'
            )
            print("✓ Conectado al Nodo 2 (MySQL - Región B)")
            
            # Nodo 3 - Oracle - Replicación
            self.conexiones['nodo3_replica'] = cx_Oracle.connect(
                user='nodo3_replica',
                password='password123',
                dsn='localhost:1521/XEPDB1'
            )
            print("✓ Conectado al Nodo 3 (Oracle - Replicación)")
            
        except Exception as e:
            print(f"Error conectando a las bases de datos: {e}")
            sys.exit(1)
    
    def ejecutar_consulta(self, nodo, query, params=None):
        """Ejecuta una consulta en el nodo especificado"""
        try:
            cursor = self.conexiones[nodo].cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                resultados = cursor.fetchall()
                cursor.close()
                return resultados
            else:
                self.conexiones[nodo].commit()
                cursor.close()
                return True
        except Exception as e:
            print(f"Error ejecutando consulta en {nodo}: {e}")
            return None
    
    def consulta_distribuida_sucursales(self, region=None):
        """Consulta distribuida de sucursales por región"""
        print("\n=== CONSULTA DISTRIBUIDA - SUCURSALES ===")
        
        if region == 'A' or region is None:
            print("\n--- Región A (Oracle) ---")
            query_a = "SELECT * FROM sucursal WHERE region = 'A'"
            resultados_a = self.ejecutar_consulta('nodo1_oracle_A', query_a)
            if resultados_a:
                for row in resultados_a:
                    print(f"ID: {row[0]}, Nombre: {row[1]}, Ciudad: {row[2]}, Activos: {row[3]}, Región: {row[4]}")
        
        if region == 'B' or region is None:
            print("\n--- Región B (MySQL) ---")
            query_b = "SELECT * FROM sucursal WHERE region = 'B'"
            resultados_b = self.ejecutar_consulta('nodo2_mysql_B', query_b)
            if resultados_b:
                for row in resultados_b:
                    print(f"ID: {row[0]}, Nombre: {row[1]}, Ciudad: {row[2]}, Activos: {row[3]}, Región: {row[4]}")
    
    def consulta_prestamos_por_sucursal(self, id_sucursal):
        """Consulta distribuida de préstamos por sucursal"""
        print(f"\n=== PRÉSTAMOS PARA SUCURSAL {id_sucursal} ===")
        
        # Determinar en qué nodo está la sucursal
        query_sucursal_a = "SELECT region FROM sucursal WHERE idsucursal = :1"
        resultado_a = self.ejecutar_consulta('nodo1_oracle_A', query_sucursal_a, (id_sucursal,))
        
        if resultado_a:
            # Está en región A
            query_prestamos = "SELECT * FROM prestamo WHERE idsucursal = :1"
            prestamos = self.ejecutar_consulta('nodo1_oracle_A', query_prestamos, (id_sucursal,))
        else:
            # Verificar en región B
            query_sucursal_b = "SELECT region FROM sucursal WHERE idsucursal = %s"
            resultado_b = self.ejecutar_consulta('nodo2_mysql_B', query_sucursal_b, (id_sucursal,))
            
            if resultado_b:
                query_prestamos = "SELECT * FROM prestamo WHERE idsucursal = %s"
                prestamos = self.ejecutar_consulta('nodo2_mysql_B', query_prestamos, (id_sucursal,))
            else:
                print("Sucursal no encontrada")
                return
        
        if prestamos:
            for prestamo in prestamos:
                print(f"Préstamo: {prestamo[0]}, Sucursal: {prestamo[1]}, Cantidad: {prestamo[2]}")
        else:
            print("No se encontraron préstamos para esta sucursal")
    
    def insertar_sucursal(self, id_sucursal, nombre, ciudad, activos, region):
        """Inserta una nueva sucursal en el nodo correspondiente"""
        print(f"\n=== INSERTANDO SUCURSAL EN REGIÓN {region} ===")
        
        if region == 'A':
            query = "INSERT INTO sucursal VALUES (:1, :2, :3, :4, :5)"
            resultado = self.ejecutar_consulta('nodo1_oracle_A', query, 
                                             (id_sucursal, nombre, ciudad, activos, region))
        elif region == 'B':
            query = "INSERT INTO sucursal VALUES (%s, %s, %s, %s, %s)"
            resultado = self.ejecutar_consulta('nodo2_mysql_B', query, 
                                             (id_sucursal, nombre, ciudad, activos, region))
        else:
            print("Región no válida. Use 'A' o 'B'")
            return
        
        if resultado:
            print(f"✓ Sucursal {id_sucursal} insertada correctamente en región {region}")
            # Replicar en nodo 3
            self.replicar_en_nodo3(id_sucursal, nombre, ciudad, activos, region, tabla='sucursal')
        else:
            print("✗ Error al insertar sucursal")
    
    def replicar_en_nodo3(self, *args, tabla):
        """Replica los datos en el nodo 3 (replicación)"""
        try:
            if tabla == 'sucursal':
                query = "INSERT INTO sucursal VALUES (:1, :2, :3, :4, :5)"
                self.ejecutar_consulta('nodo3_replica', query, args)
                print(f"✓ Datos replicados en Nodo 3")
            elif tabla == 'prestamo':
                query = "INSERT INTO prestamo VALUES (:1, :2, :3)"
                self.ejecutar_consulta('nodo3_replica', query, args)
                print(f"✓ Préstamo replicado en Nodo 3")
        except Exception as e:
            print(f"Error en replicación: {e}")
    
    def consulta_global_activos(self):
        """Consulta global de activos por región"""
        print("\n=== CONSULTA GLOBAL - ACTIVOS POR REGIÓN ===")
        
        # Región A
        query_a = "SELECT region, SUM(activos) as total_activos FROM sucursal WHERE region = 'A' GROUP BY region"
        resultado_a = self.ejecutar_consulta('nodo1_oracle_A', query_a)
        
        # Región B
        query_b = "SELECT region, SUM(activos) as total_activos FROM sucursal WHERE region = 'B' GROUP BY region"
        resultado_b = self.ejecutar_consulta('nodo2_mysql_B', query_b)
        
        print("\nResumen de Activos:")
        if resultado_a:
            print(f"Región A: ${resultado_a[0][1]:,}")
        if resultado_b:
            print(f"Región B: ${resultado_b[0][1]:,}")
    
    def verificar_consistencia(self):
        """Verifica la consistencia entre nodos"""
        print("\n=== VERIFICACIÓN DE CONSISTENCIA ===")
        
        # Contar registros en cada nodo
        count_a = self.ejecutar_consulta('nodo1_oracle_A', "SELECT COUNT(*) FROM sucursal")
        count_b = self.ejecutar_consulta('nodo2_mysql_B', "SELECT COUNT(*) FROM sucursal")
        count_replica = self.ejecutar_consulta('nodo3_replica', "SELECT COUNT(*) FROM sucursal")
        
        print(f"Sucursales en Nodo 1 (Región A): {count_a[0][0] if count_a else 0}")
        print(f"Sucursales en Nodo 2 (Región B): {count_b[0][0] if count_b else 0}")
        print(f"Sucursales en Nodo 3 (Réplica): {count_replica[0][0] if count_replica else 0}")
        
        total_distribuido = (count_a[0][0] if count_a else 0) + (count_b[0][0] if count_b else 0)
        total_replica = count_replica[0][0] if count_replica else 0
        
        if total_distribuido == total_replica:
            print("✓ Consistencia verificada - Los datos están sincronizados")
        else:
            print("✗ Inconsistencia detectada - Los datos no están sincronizados")
    
    def cerrar_conexiones(self):
        """Cierra todas las conexiones"""
        for nombre, conexion in self.conexiones.items():
            try:
                conexion.close()
                print(f"✓ Conexión {nombre} cerrada")
            except:
                pass

def menu_principal():
    """Menú principal de la aplicación"""
    bd = BaseDatosDistribuida()
    
    while True:
        print("\n" + "="*50)
        print("SISTEMA DE BASE DE DATOS DISTRIBUIDA - BANCOS")
        print("="*50)
        print("1. Consultar todas las sucursales")
        print("2. Consultar sucursales por región")
        print("3. Consultar préstamos por sucursal")
        print("4. Insertar nueva sucursal")
        print("5. Consulta global de activos")
        print("6. Verificar consistencia")
        print("7. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == '1':
            bd.consulta_distribuida_sucursales()
        
        elif opcion == '2':
            region = input("Ingrese la región (A/B): ").upper()
            if region in ['A', 'B']:
                bd.consulta_distribuida_sucursales(region)
            else:
                print("Región no válida")
        
        elif opcion == '3':
            id_sucursal = input("Ingrese el ID de la sucursal: ")
            bd.consulta_prestamos_por_sucursal(id_sucursal)
        
        elif opcion == '4':
            print("\n--- Insertar Nueva Sucursal ---")
            id_suc = input("ID Sucursal: ")
            nombre = input("Nombre: ")
            ciudad = input("Ciudad: ")
            activos = float(input("Activos: "))
            region = input("Región (A/B): ").upper()
            
            if region in ['A', 'B']:
                bd.insertar_sucursal(id_suc, nombre, ciudad, activos, region)
            else:
                print("Región no válida")
        
        elif opcion == '5':
            bd.consulta_global_activos()
        
        elif opcion == '6':
            bd.verificar_consistencia()
        
        elif opcion == '7':
            bd.cerrar_conexiones()
            print("¡Hasta luego!")
            break
        
        else:
            print("Opción no válida")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    menu_principal()
