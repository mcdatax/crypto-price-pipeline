from config.crypto_config import COINGECKO_API_KEY
from pipelines.crypto.extract import extract_prices
from pipelines.crypto.transform import transform_prices
from pipelines.crypto.load import load_prices
from db.sqlite import create_tables


def run():
    """
    Función principal para ejecutar el pipeline de criptomonedas.
    Se encarga de obtener los datos, procesarlos y almacenarlos en la DB.
    """
    DB_PATH = "crypto_prices.db" # Ruta a la base de datos SQLite

    # Primero: garantizar que la DB y tablas existen
    create_tables(DB_PATH)

    print("Iniciando pipeline de criptomonedas...")

    # Paso 1: Obtener datos de CoinGecko
    print("Obteniendo datos de CoinGecko...")
    try:
        data = extract_prices(COINGECKO_API_KEY)
        print("Datos obtenidos exitosamente.")
    except Exception as e:
        print(f"Error al obtener datos: {e}")
        return
    
    # Paso 2: Procesar y almacenar datos en la DB
    print("Procesando y almacenando datos en la DB...")
    try:
        transformed_data = transform_prices(data)
        load_prices(transformed_data, DB_PATH)
        print("Datos procesados y almacenados correctamente.")
    except Exception as e:
        print(f"Error al procesar/almacenar datos: {e}")
        return

    print("Pipeline de criptomonedas finalizado exitosamente.")



if __name__ == "__main__":
    run() 