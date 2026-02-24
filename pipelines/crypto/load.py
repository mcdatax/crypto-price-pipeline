from db.sqlite import get_connection, get_or_create_coin, insert_price_log


def load_prices(transformed_data: list, db_path: str) -> None:
    """
    Carga los datos transformados en la base de datos SQLite.
    Para cada tupla (coin_name, price, timestamp), obtiene o crea el ID de la moneda y luego inserta el registro de precio.

    Args:
        transformed_data (list of tuples): Lista de tuplas con el formato (coin_name, price, timestamp).
        db_path (str): Ruta al archivo de la base de datos SQLite.
    """
    conn = get_connection(db_path)

    for coin_name, price, captured_at in transformed_data:
        # Obtiene o crea el ID de la moneda
        coin_id = get_or_create_coin(conn, coin_name)
        # Inserta el registro de precio
        insert_price_log(conn, coin_id, price, captured_at)

    conn.commit()  # Guarda todos los cambios realizados
    conn.close()   # Cierra la conexión a la base de datos
    print(f"Datos cargados exitosamente en: {db_path}")