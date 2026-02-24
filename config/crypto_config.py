# crypto_usd_config.py
# Este archivo carga las credenciales desde variables de entorno de forma segura

# Importar la librería 'os' para acceder a las variables de entorno del sistema
import os

# Importar 'load_dotenv' para cargar el archivo .env automáticamente
from dotenv import load_dotenv

# Cargar las variables del archivo .env al entorno del sistema
# Esto lee el archivo .env y hace disponibles las variables
load_dotenv()

# Obtener cada credencial desde las variables de entorno
# os.getenv('NOMBRE_VARIABLE') busca la variable en el entorno
# Si no la encuentra, devuelve None (o el valor por defecto que indiques)

# Credencial 1: API Key de CoinGecko
COINGECKO_API_KEY = os.getenv('COINGECKO_API_KEY')

# Opcional: Verificar que todas las credenciales fueron cargadas correctamente
# Esto te avisará si falta alguna variable en tu archivo .env
if not all([COINGECKO_API_KEY]):
    print("⚠️  ADVERTENCIA: Faltan algunas credenciales en tu archivo .env")
    print("Asegúrate de que tu archivo .env contiene todas las variables necesarias")
