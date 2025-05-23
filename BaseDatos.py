
import psycopg2
from psycopg2 import sql

class BaseDatos:
    def __init__(self, nombre_db="tienda", usuario="postgres", contraseña="chinoloco", host="localhost", puerto="5432"):
        self.nombre_db = nombre_db
        self.usuario = usuario
        self.contraseña = contraseña
        self.host = host
        self.puerto = puerto
        self._crear_tablas()

    def conectar(self):
        return psycopg2.connect(
            dbname=self.nombre_db,
            user=self.usuario,
            password=self.contraseña,
            host=self.host,
            port=self.puerto
        )

    def _crear_tablas(self):
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        nivel INTEGER NOT NULL
    )
''')


        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id VARCHAR PRIMARY KEY,
                nombre TEXT,
                direccion TEXT,
                telefono TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS proveedores (
                id VARCHAR PRIMARY KEY,
                cod_prod TEXT,
                descripcion TEXT,
                costo TEXT,
                direccion TEXT,
                telefono TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventarios (
                cod VARCHAR PRIMARY KEY,
                cantidad TEXT,
                stock TEXT,
                precio TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas (
                id SERIAL PRIMARY KEY,
                id_cliente VARCHAR,
                cod_prod TEXT,
                cantidad TEXT,
                descripcion TEXT,
                iva REAL,
                subtotal REAL,
                total REAL
            )
        ''')

        conn.commit()
        cursor.close()
        conn.close()
