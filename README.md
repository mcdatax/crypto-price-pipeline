<div align="center">

# 🚀 Data Pipelines — Weather & Crypto

### Pipelines de Ingeniería de Datos construidos con buenas prácticas reales
*ETL modular · SQLite normalizado · Alertas SMS · Arquitectura escalable*

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Twilio](https://img.shields.io/badge/Twilio-SMS-F22F46?logo=twilio&logoColor=white)](https://www.twilio.com/)
[![WeatherAPI](https://img.shields.io/badge/WeatherAPI-Forecast-00BFFF)](https://www.weatherapi.com/)
[![CoinGecko](https://img.shields.io/badge/CoinGecko-Crypto-8DC63F?logo=bitcoin&logoColor=white)](https://www.coingecko.com/)
[![DolarAPI](https://img.shields.io/badge/DolarAPI-USD/COP-FFD700)](https://dolarapi.com/)

[Descripción](#-descripción) • [Arquitectura](#-arquitectura-etl) • [Pipelines](#-pipelines) • [Instalación](#-instalación) • [Uso](#-uso) • [Buenas Prácticas](#-buenas-prácticas)

</div>


---

## 📖 Descripción

Este repositorio contiene **dos pipelines de datos independientes** construidos siguiendo las convenciones y buenas prácticas reales de la industria de **Data Engineering**:

| Pipeline | Fuente de datos | Destino | Frecuencia |
|---|---|---|---|
| 🌤️ **Weather** | WeatherAPI | Alertas SMS (Twilio) | 1 vez al día |
| 📈 **Crypto** | CoinGecko + DolarAPI | SQLite (histórico) | Cada hora |

Cada pipeline sigue el patrón **ETL** (Extract → Transform → Load), con separación clara de responsabilidades, módulos reutilizables y una base de datos relacional normalizada.

---

## 🏗️ Arquitectura ETL

El patrón **ETL** es el estándar en ingeniería de datos. Cada fase tiene una única responsabilidad:

```
┌─────────────┐     ┌─────────────────┐     ┌─────────────┐
│   EXTRACT   │────▶│    TRANSFORM    │────▶│    LOAD     │
│             │     │                 │     │             │
│ Obtiene los │     │ Limpia, da      │     │ Persiste en │
│ datos crudos│     │ formato y agrega│     │ el destino  │
│ de la fuente│     │ metadata        │     │ final       │
└─────────────┘     └─────────────────┘     └─────────────┘
```

> **¿Por qué separar en 3 fases?**
> Si mañana cambias la API de precios, solo tocas `extract.py`. Si cambias la DB de SQLite a PostgreSQL, solo tocas `load.py`. El resto del pipeline no se entera. Eso es **desacoplamiento**.

---

## 📂 Estructura del Proyecto

```
Pipeline_weather/
│
├── 📁 pipelines/
│   ├── 🌤️ weather/
│   │   ├── extract.py        # Consulta WeatherAPI
│   │   ├── transform.py      # Filtra horas con lluvia
│   │   └── load.py           # Envía SMS via Twilio
│   │
│   └── 📈 crypto/
│       ├── extract.py        # Consulta CoinGecko + DolarAPI
│       ├── transform.py      # Estructura datos + agrega timestamp
│       └── load.py           # Inserta en SQLite
│
├── 📁 db/
│   └── sqlite.py             # Funciones puras de base de datos
│
├── 📁 config/
│   └── crypto_config.py      # Carga credenciales desde .env
│
├── run_crypto.py             # Orquestador del pipeline crypto
├── twilio_script.py          # Orquestador del pipeline weather
├── .env                      # ⚠️ Credenciales (NO se sube a git)
├── .env.example              # Plantilla de variables de entorno
└── requirements.txt          # Dependencias del proyecto
```

---

## 🔌 Pipelines

### 📈 Pipeline Crypto — Histórico de precios

Captura cada hora el precio en USD de las **top 20 criptomonedas** por capitalización de mercado (vía CoinGecko) y el tipo de cambio **USD/COP** (vía DolarAPI), guardándolos en una base de datos SQLite normalizada para su análisis posterior.

**Flujo:**
```
CoinGecko API ──┐
                ├──▶ extract_prices() ──▶ transform_prices() ──▶ load_prices() ──▶ SQLite DB
DolarAPI ───────┘
```

**Ejecución:**
```bash
python run_crypto.py
```

---

### 🌤️ Pipeline Weather — Alertas de lluvia

Consulta el pronóstico del día para una ciudad y envía un **SMS automático** con las horas exactas en que se espera lluvia. Solo alerta entre las 6 AM y 10 PM.

**Flujo:**
```
WeatherAPI ──▶ request_wapi() ──▶ create_df() ──▶ send_message() ──▶ SMS Twilio
```

**Ejecución:**
```bash
python twilio_script.py
```

---

## 🗄️ Base de Datos — Diseño Normalizado

La DB del pipeline crypto está **normalizada** para evitar redundancia y garantizar integridad:

```
┌──────────────┐          ┌────────────────────┐
│    coins     │          │    price_logs       │
├──────────────┤          ├────────────────────┤
│ id (PK) 🔑  │◄────┐    │ id (PK) 🔑         │
│ name (UNIQUE)│     └────│ coin_id (FK) 🔗    │
└──────────────┘          │ price              │
                          │ captured_at        │
                          └────────────────────┘
```

**¿Por qué esta estructura?**
- `coins` es la **tabla maestra** — cada moneda se registra **una sola vez**, sin importar cuántos precios se capturen.
- `price_logs` guarda el **histórico** con una fila por moneda por captura.
- La **Foreign Key** garantiza integridad referencial: no puede existir un precio sin su moneda.
- Si aparece una moneda nueva en CoinGecko, `get_or_create_coin()` la registra **automáticamente**.

Después de una semana de capturas cada hora:

> 21 activos × 24 horas × 7 días = **3,528 registros** — perfectamente manejable en SQLite.

---

## 🛠️ Tecnologías

| Categoría | Tecnología | Uso |
|---|---|---|
| **Lenguaje** | ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white) | Todo el proyecto |
| **Base de datos** | ![SQLite](https://img.shields.io/badge/-SQLite-003B57?logo=sqlite&logoColor=white) | Histórico de precios |
| **APIs de datos** | CoinGecko · WeatherAPI · DolarAPI | Fuentes de datos |
| **Notificaciones** | ![Twilio](https://img.shields.io/badge/-Twilio-F22F46?logo=twilio&logoColor=white) | Alertas SMS |
| **Data** | ![Pandas](https://img.shields.io/badge/-Pandas-150458?logo=pandas&logoColor=white) | Procesamiento tabular |
| **HTTP** | Requests | Llamadas a APIs |
| **Seguridad** | python-dotenv | Gestión de credenciales |

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/mcdatax/Pipeline_weather.git
cd Pipeline_weather
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar credenciales

Copia el archivo de ejemplo y rellena tus keys:

```bash
cp .env.example .env
```

```env
# .env — NUNCA subas este archivo a git
COINGECKO_API_KEY=tu_api_key_aqui
TWILIO_ACCOUNT_SID=tu_account_sid
TWILIO_AUTH_TOKEN=tu_auth_token
TWILIO_PHONE_NUMBER=+1234567890
PHONE_NUMBER_DESTINATION=+57300000000
API_KEY_WAPI=tu_weatherapi_key
```

> ⚠️ El archivo `.env` ya está en `.gitignore`. Nunca lo subas a un repositorio público.

---

## 💻 Uso

### Pipeline Crypto (histórico de precios)

```bash
# Una ejecución manual
python run_crypto.py

# Automatizar cada hora con cron (macOS/Linux)
crontab -e
# Añadir esta línea:
0 * * * * cd /ruta/al/proyecto && .venv/bin/python run_crypto.py
```

### Pipeline Weather (alerta diaria)

```bash
# Una ejecución manual
python twilio_script.py

# Automatizar cada día a las 7 AM con cron
0 7 * * * cd /ruta/al/proyecto && .venv/bin/python twilio_script.py
```

### Analizar el histórico con pandas

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect("crypto_prices.db")

# Ver todos los precios de Bitcoin
df = pd.read_sql("""
    SELECT p.captured_at, p.price
    FROM price_logs p
    JOIN coins c ON c.id = p.coin_id
    WHERE c.name = 'Bitcoin'
    ORDER BY p.captured_at
""", conn)

conn.close()
print(df)
```

---

## ✅ Buenas Prácticas aplicadas

Este proyecto fue construido siguiendo los estándares reales de la industria:

- **📦 Separación por módulos** — cada archivo tiene una única responsabilidad (principio SRP)
- **🔒 Credenciales en `.env`** — ninguna API key hardcodeada en el código
- **🗂️ Imports absolutos** — `from db.sqlite import ...` siempre desde la raíz
- **🧩 Funciones puras** — sin efectos secundarios ocultos, fáciles de testear
- **🔗 DB normalizada** — sin redundancia, con Foreign Keys e integridad referencial
- **⚛️ Transacciones atómicas** — el `commit()` va después de todas las inserciones, no dentro del loop
- **🛡️ SQL parametrizado** — uso de `?` en lugar de f-strings para prevenir SQL injection
- **📝 Type hints** — `def load_prices(data: list, db_path: str) -> None`
- **📋 Docstrings** — cada función documenta qué recibe, qué hace y qué retorna
- **🏷️ `if __name__ == "__main__"`** — los scripts son ejecutables e importables

---

## 📦 Dependencias

```
requests>=2.28.0         # Llamadas HTTP a las APIs
pandas>=1.5.0            # Procesamiento de datos
twilio>=8.0.0            # Envío de SMS
python-dotenv>=0.21.0    # Carga de variables de entorno
beautifulsoup4>=4.11.0   # Parsing HTML
tqdm>=4.64.0             # Barras de progreso
```

---

## 🗺️ Roadmap

- [x] Pipeline Weather con alertas SMS
- [x] Pipeline Crypto con histórico en SQLite normalizada
- [x] Arquitectura ETL modular por capas
- [ ] Scheduler automático con APScheduler
- [ ] Logging estructurado (reemplazar `print()` por `logging`)
- [ ] Tests unitarios con `pytest`
- [ ] Análisis y visualización del histórico
- [ ] Migración a PostgreSQL para mayor escala
- [ ] Despliegue en AWS Lambda / Azure Functions

---

## 👤 Autor

**mcdatax**

[![GitHub](https://img.shields.io/badge/GitHub-mcdatax-181717?logo=github)](https://github.com/mcdatax)

---

<div align="center">

**⭐ Si te resulta útil, dale una estrella al repositorio ⭐**

[🐛 Reportar Bug](https://github.com/mcdatax/Pipeline_weather/issues) • [💡 Solicitar Feature](https://github.com/mcdatax/Pipeline_weather/issues)

</div>
