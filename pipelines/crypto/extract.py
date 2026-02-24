import warnings
import requests

# Suprime el warning de compatibilidad SSL de urllib3 en macOS con LibreSSL
warnings.filterwarnings("ignore", category=Warning)


def extract_prices(api_key):

    # url = f'https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids={cryptocurrency}&x_cg_demo_api_key={api_key}'
    url = f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=20&page=1&x_cg_demo_api_key={api_key}' # URL de la API de CoinGecko para obtener el precio actual de la criptomoneda especificada en dólares estadounidenses (USD)
    try :
        response = requests.get(url).json()
        coins = {coin['name']: round(float(coin['current_price']), 2) for coin in response}
        url = 'https://co.dolarapi.com/v1/cotizaciones/usd'
        usd_cop = requests.get(url).json()
        coins["USD_COP"] = round(float(usd_cop['compra']), 2)
    except Exception as e:
        print(e)
    
    return coins