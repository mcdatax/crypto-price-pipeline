import pymysql
import pymysql.cursors
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection() -> pymysql.connections.Connection:
    """
    Abre y retorna una conexión a la base de datos MySQL.
    Lee las credenciales desde variables de entorno.

    Returns:
        pymysql.connections.Connection: Objeto de conexión activo
    """
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )


def create_tables() -> None:
    """
    Crea las tablas 'coins' y 'price_logs' si no existen.
    Se ejecuta una sola vez al inicializar el pipeline.
    """
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS coins (
                id   INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                UNIQUE KEY unique_name (name)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS price_logs (
                id          INT AUTO_INCREMENT PRIMARY KEY,
                coin_id     INT NOT NULL,
                price       FLOAT NOT NULL,
                captured_at DATETIME NOT NULL,
                FOREIGN KEY (coin_id) REFERENCES coins(id)
            )
        """)
    conn.commit()
    conn.close()
    print(f"Tablas listas en MySQL: {os.getenv('MYSQL_DATABASE')}")


def get_or_create_coin(conn: pymysql.connections.Connection, name: str) -> int:
    """
    Busca una moneda por nombre. Si no existe, la inserta.
    Retorna siempre el id de la moneda.

    Args:
        conn: Conexión activa a MySQL
        name (str): Nombre de la moneda (ej. "Bitcoin")

    Returns:
        int: ID de la moneda en la tabla coins
    """
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM coins WHERE name = %s", (name,))
        row = cursor.fetchone()
        if row:
            return row["id"]

        cursor.execute("INSERT INTO coins (name) VALUES (%s)", (name,))
        return cursor.lastrowid


def insert_price_log(conn: pymysql.connections.Connection, coin_id: int, price: float, captured_at: str) -> None:
    """
    Inserta un registro de precio en price_logs.

    Args:
        conn: Conexión activa a MySQL
        coin_id (int): ID de la moneda (FK a coins.id)
        price (float): Precio en USD
        captured_at (str): Timestamp, ej. "2026-02-24 15:00:00"
    """
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO price_logs (coin_id, price, captured_at) VALUES (%s, %s, %s)",
            (coin_id, price, captured_at)
        )
