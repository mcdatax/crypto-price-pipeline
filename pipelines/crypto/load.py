import db.factory as db


def load_prices(transformed_data: list) -> None:
    """
    Carga los datos transformados en la base de datos activa (SQLite o MySQL).
    El motor se selecciona automáticamente según DB_ENGINE en el archivo .env.

    Args:
        transformed_data (list of tuples): Lista de tuplas con el formato (coin_name, price, timestamp).
    """
    conn = db.get_connection()

    for coin_name, price, captured_at in transformed_data:
        coin_id = db.get_or_create_coin(conn, coin_name)
        db.insert_price_log(conn, coin_id, price, captured_at)

    db.commit_and_close(conn)
    print("Datos cargados exitosamente en la base de datos.")