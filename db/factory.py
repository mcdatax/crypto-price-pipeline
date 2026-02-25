"""
db/factory.py
Selecciona automáticamente el motor de base de datos según la variable de entorno DB_ENGINE.

Uso en .env:
  DB_ENGINE=sqlite   → usa SQLite (desarrollo local)
  DB_ENGINE=mysql    → usa MySQL  (producción en EC2)
"""
import os
from dotenv import load_dotenv

load_dotenv()

DB_ENGINE = os.getenv("DB_ENGINE", "sqlite").lower()
SQLITE_PATH = os.getenv("SQLITE_PATH", "crypto_prices.db")

if DB_ENGINE == "mysql":
    import db.mysql as _db

    def create_tables():
        return _db.create_tables()

    def get_connection():
        return _db.get_connection()

    def get_or_create_coin(conn, name: str) -> int:
        return _db.get_or_create_coin(conn, name)

    def insert_price_log(conn, coin_id: int, price: float, captured_at: str) -> None:
        return _db.insert_price_log(conn, coin_id, price, captured_at)

    def commit_and_close(conn) -> None:
        conn.commit()
        conn.close()

else:  # sqlite (default)
    import db.sqlite as _db

    def create_tables():
        return _db.create_tables(SQLITE_PATH)

    def get_connection():
        return _db.get_connection(SQLITE_PATH)

    def get_or_create_coin(conn, name: str) -> int:
        return _db.get_or_create_coin(conn, name)

    def insert_price_log(conn, coin_id: int, price: float, captured_at: str) -> None:
        return _db.insert_price_log(conn, coin_id, price, captured_at)

    def commit_and_close(conn) -> None:
        conn.commit()
        conn.close()

print(f"[DB] Motor activo: {DB_ENGINE.upper()}")
