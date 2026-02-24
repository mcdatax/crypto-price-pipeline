import datetime as dt

def transform_prices(raw: dict) -> list:
    """
    Transforma los datos de precios en un formato adecuado para la inserción en la base de datos.
    Convierte el diccionario de precios a una lista de tuplas (coin_name, price).

    Args:
        raw (dict): Diccionario con nombres de monedas como claves y precios como valores.

    Returns:
        list of tuples: Lista de tuplas con el formato (coin_name, price, timestamp).
    """
    transformed_data = []
    captured_at = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Timestamp actual para todas las monedas
    
    for coin_name, price in raw.items():
        transformed_data.append((coin_name, price, captured_at)) # Agrega una tupla con el nombre de la moneda, su precio y el timestamp
    
    return transformed_data