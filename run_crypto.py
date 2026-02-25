from config.crypto_config import COINGECKO_API_KEY
from pipelines.crypto.extract import extract_prices
from pipelines.crypto.transform import transform_prices
from pipelines.crypto.load import load_prices
import db.factory as db


def run():
    """
    Función principal para ejecutar el pipeline de criptomonedas.
    El motor de DB (SQLite o MySQL) se selecciona automáticamente según DB_ENGINE en .env.
    """
    # Garantizar que las tablas existen en el motor activo
    db.create_tables()

    print("Iniciando pipeline de criptomonedas...")

    # Paso 1: Obtener datos de CoinGecko
    print("Obteniendo datos de CoinGecko...")
    try:
        data = extract_prices(COINGECKO_API_KEY)
        print("Datos obtenidos exitosamente.")
    except Exception as e:
        print(f"Error al obtener datos: {e}")
        return

    # Paso 2: Transformar y cargar en DB
    print("Procesando y almacenando datos en la DB...")
    try:
        transformed_data = transform_prices(data)
        load_prices(transformed_data)
        print("Datos procesados y almacenados correctamente.")
    except Exception as e:
        print(f"Error al procesar/almacenar datos: {e}")
        return

    print("Pipeline de criptomonedas finalizado exitosamente.")



if __name__ == "__main__":
    run() 