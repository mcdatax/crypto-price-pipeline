import warnings
import requests

# Suprime el warning de compatibilidad SSL de urllib3 en macOS con LibreSSL
warnings.filterwarnings("ignore", category=Warning)


def extract_prices(api_key):

    url_coingecko = (
        f'https://api.coingecko.com/api/v3/coins/markets'
        f'?vs_currency=usd&order=market_cap_desc&per_page=20&page=1'
        f'&x_cg_demo_api_key={api_key}'
    )
    url_dolar = 'https://co.dolarapi.com/v1/cotizaciones/usd'
    coins = {}

    try:
        response = requests.get(url_coingecko, timeout=15).json()
        coins = {coin['name']: round(float(coin['current_price']), 2) for coin in response}
    except Exception as e:
        print(f"[ERROR] CoinGecko: {e}")

    try:
        usd_cop = requests.get(url_dolar, timeout=10).json()
        coins["USD_COP"] = round(float(usd_cop['compra']), 2)
    except Exception as e:
        print(f"[WARN] DolarAPI no disponible, se omite USD_COP: {e}")

    return coins