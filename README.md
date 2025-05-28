# Banco
# Sistema de Base de Datos Distribuida - Bancos

Un sistema de base de datos distribuida que simula la gestión de sucursales bancarias y préstamos distribuidos geográficamente en diferentes nodos con replicación automática.

## 📋 Descripción

Este proyecto implementa un sistema de base de datos distribuida que maneja información de sucursales bancarias distribuidas en dos regiones geográficas diferentes, con un tercer nodo que actúa como réplica completa del sistema. El sistema permite realizar consultas distribuidas, mantener consistencia de datos y manejar transacciones entre múltiples gestores de bases de datos.

## 🏗️ Arquitectura del Sistema

### Nodos de la Base de Datos:

- **Nodo 1 (Oracle)** - Región A: Gestiona sucursales de la región A
- **Nodo 2 (MySQL)** - Región B: Gestiona sucursales de la región B  
- **Nodo 3 (Oracle)** - Nodo de Replicación: Mantiene una copia completa de ambas regiones

### Esquema de Datos:

```sql
sucursal:
- idsucursal (VARCHAR/VARCHAR2)
- nombresucursal (VARCHAR/VARCHAR2) 
- ciudadsucursal (VARCHAR/VARCHAR2)
- activos (DECIMAL/NUMBER)
- region (VARCHAR/VARCHAR2)

prestamo:
- noprestamo (VARCHAR/VARCHAR2)
- idsucursal (VARCHAR/VARCHAR2) [FK]
- cantidad (DECIMAL/NUMBER)
```

## 🛠️ Tecnologías Utilizadas

- **Python 3.x**
- **Oracle Database** (Nodos 1 y 3)
- **MySQL** (Nodo 2)
- **Librerías Python:**
  - `cx_Oracle` - Conectividad con Oracle
  - `mysql-connector-python` - Conectividad con MySQL

## 📦 Instalación

### Prerrequisitos

1. **Oracle Database** instalado y configurado
2. **MySQL Server** instalado y configurado
3. **Python 3.x** instalado

### Instalar dependencias

```bash
pip install cx_Oracle mysql-connector-python
```

### Configurar Oracle Client (si es necesario)

```bash
# Para Oracle Instant Client
export LD_LIBRARY_PATH=/path/to/instantclient:$LD_LIBRARY_PATH
```

## ⚙️ Configuración

### 1. Configurar Oracle (Nodos 1 y 3)

Ejecutar los siguientes scripts SQL en Oracle:

```bash
# Para Nodo 1 (Región A)
sqlplus sys/password@localhost:1521/XEPDB1 as sysdba @Nodo1.sql

# Para Nodo 3 (Réplica)
sqlplus sys/password@localhost:1521/XEPDB1 as sysdba @Nodo3.sql
```

### 2. Configurar MySQL (Nodo 2)

```bash
# Ejecutar script para Nodo 2 (Región B)
mysql -u root -p < Nodo2.sql
```

### 3. Ajustar Parámetros de Conexión

Editar el archivo `banco.py` y ajustar las credenciales de conexión según tu configuración:

```python
# Nodo 1 - Oracle
self.conexiones['nodo1_oracle_A'] = cx_Oracle.connect(
    user='nodo1_regionA',
    password='tu_password',
    dsn='tu_host:1521/XEPDB1'
)

# Nodo 2 - MySQL  
self.conexiones['nodo2_mysql_B'] = mysql.connector.connect(
    host='tu_host',
    database='nodo2_regionB',
    user='tu_usuario',
    password='tu_password'
)
```

## 🚀 Uso

### Inicialización de Datos

Ejecutar el script de inicialización para poblar los nodos con datos de prueba:

```bash
python init_datos.py
```

### Ejecutar la Aplicación Principal

```bash
python banco.py
```

### Menú de Opciones

El sistema ofrece las siguientes funcionalidades:

1. **Consultar todas las sucursales** - Vista global de todas las sucursales
2. **Consultar sucursales por región** - Filtrar por región A o B
3. **Consultar préstamos por sucursal** - Ver préstamos de una sucursal específica
4. **Insertar nueva sucursal** - Agregar sucursal con replicación automática
5. **Consulta global de activos** - Resumen de activos por región
6. **Verificar consistencia** - Validar sincronización entre nodos

## 📁 Estructura del Proyecto

```
├── banco.py           # Aplicación principal con lógica distribuida
├── init_datos.py      # Script de inicialización de datos
├── Nodo1.sql         # Script SQL para Oracle Nodo 1 (Región A)
├── Nodo2.sql         # Script SQL para MySQL Nodo 2 (Región B)  
├── Nodo3.sql         # Script SQL para Oracle Nodo 3 (Réplica)
└── README.md         # Este archivo
```

## 🎯 Características Principales

### Distribución Geográfica
- **Región A**: Sucursales S0001-S0004 en Oracle
- **Región B**: Sucursales S0005-S0009 en MySQL

### Replicación Automática
- Todas las inserciones se replican automáticamente en el Nodo 3
- Verificación de consistencia entre nodos

### Consultas Distribuidas
- Búsqueda automática en el nodo correcto según la región
- Agregación de datos de múltiples nodos

### Gestión de Transacciones
- Manejo de errores y rollback automático
- Verificación de integridad referencial

## 📊 Datos de Ejemplo

El sistema incluye datos de prueba con:
- **9 sucursales** distribuidas en 2 regiones
- **9 préstamos** asociados a diferentes sucursales
- **Activos totales** superiores a $23 millones

### Región A (Oracle):
- Downtown, Redwood, Perryridge, Mianus
- Total activos: ~$5.1M

### Región B (MySQL):
- Round Hill, Pownal, North Town, Brighton, Central  
- Total activos: ~$18.5M

## 🔧 Troubleshooting

### Errores Comunes

**Error de conexión Oracle:**
```
ORA-12541: TNS:no listener
```
- Verificar que Oracle esté ejecutándose
- Revisar la configuración de TNS

**Error de conexión MySQL:**
```
mysql.connector.errors.InterfaceError
```
- Verificar credenciales de MySQL
- Confirmar que el servicio MySQL esté activo

**Error de dependencias:**
```
ModuleNotFoundError: No module named 'cx_Oracle'
```
- Instalar dependencias: `pip install cx_Oracle mysql-connector-python`

## 👥 Autores

Moises Aaron Bustillos Sandoval – 361352  
Emiliano Herrera Domínguez – 353259  
Guillermo Cruz Juárez - 352905 
