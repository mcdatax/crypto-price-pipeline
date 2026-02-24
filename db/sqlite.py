import sqlite3


def get_connection(db_path: str) -> sqlite3.Connection:
    """
    Abre y retorna una conexión a la base de datos SQLite.
    El llamador es responsable de hacer commit y cerrar la conexión.

    Args:
        db_path (str): Ruta al archivo .db

    Returns:
        sqlite3.Connection: Objeto de conexión activo
    """
    return sqlite3.connect(db_path)


def create_tables(db_path: str) -> None:
    """
    Crea las tablas 'coins' y 'price_logs' si no existen.
    Se ejecuta una sola vez al inicializar el pipeline.

    Args:
        db_path (str): Ruta al archivo .db
    """
    conn = get_connection(db_path)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS coins (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            UNIQUE(name)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS price_logs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            coin_id     INTEGER NOT NULL,
            price       REAL NOT NULL,
            captured_at TEXT NOT NULL,
            FOREIGN KEY (coin_id) REFERENCES coins(id)
        )
    """)

    conn.commit() # Guarda ambas creaciones como una sola operación atómica
    conn.close()
    print(f"Tablas listas en: {db_path}")


def get_or_create_coin(conn: sqlite3.Connection, name: str) -> int:
    """
    Busca una moneda por nombre. Si no existe, la inserta.
    Retorna siempre el id de la moneda.

    Args:
        conn (sqlite3.Connection): Conexión activa a la DB
        name (str): Nombre de la moneda (ej. "Bitcoin")

    Returns:
        int: ID de la moneda en la tabla coins
    """
    # Intenta encontrar la moneda
    row = conn.execute(
        "SELECT id FROM coins WHERE name = ?", (name,)
    ).fetchone()

    if row:
        return row[0]  # Ya existe, retorna su id

    # No existe, la inserta y retorna el id generado
    cursor = conn.execute(
        "INSERT INTO coins (name) VALUES (?)", (name,)
    )
    return cursor.lastrowid  # ID autoasignado por SQLite en el INSERT


def insert_price_log(conn: sqlite3.Connection, coin_id: int, price: float, captured_at: str) -> None:
    """
    Inserta un registro de precio en price_logs.

    Args:
        conn (sqlite3.Connection): Conexión activa a la DB
        coin_id (int): ID de la moneda (FK a coins.id)
        price (float): Precio en USD
        captured_at (str): Timestamp ISO 8601, ej. "2026-02-24 15:00:00"
    """
    conn.execute(
        "INSERT INTO price_logs (coin_id, price, captured_at) VALUES (?, ?, ?)",
        (coin_id, price, captured_at)
    )
