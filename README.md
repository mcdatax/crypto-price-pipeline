<div align="center">

# 📈 Crypto Price Pipeline

### Pipeline de Ingeniería de Datos — Histórico de precios de criptomonedas
*ETL modular · SQLite normalizado · Arquitectura escalable · Buenas prácticas reales*

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![CoinGecko](https://img.shields.io/badge/CoinGecko-Top%2020%20Cryptos-8DC63F?logo=bitcoin&logoColor=white)](https://www.coingecko.com/)
[![DolarAPI](https://img.shields.io/badge/DolarAPI-USD%2FCOP-FFD700)](https://dolarapi.com/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)

[Descripción](#-descripción) • [Arquitectura](#-arquitectura-etl) • [Estructura](#-estructura-del-proyecto) • [DB](#-base-de-datos) • [Instalación](#-instalación) • [Uso](#-uso) • [Buenas Prácticas](#-buenas-prácticas)

</div>

---

## 📖 Descripción

**Crypto Price Pipeline** captura automáticamente el precio en USD de las **top 20 criptomonedas** por capitalización de mercado (vía CoinGecko) y el tipo de cambio **USD/COP** (vía DolarAPI), almacenándolos en una base de datos SQLite normalizada para análisis histórico.

Construido siguiendo el patrón estándar de la industria **ETL** (Extract → Transform → Load), con separación clara de responsabilidades, funciones puras, base de datos relacional normalizada y gestión segura de credenciales.

---

## 🏗️ Arquitectura ETL

El patrón **ETL** es el estándar en ingeniería de datos. Cada fase tiene una única responsabilidad:

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│     EXTRACT     │────▶│      TRANSFORM       │────▶│      LOAD       │
│                 │     │                      │     │                 │
│  CoinGecko API  │     │  Estructura datos    │     │  Persiste en    │
│  DolarAPI       │     │  Agrega timestamp    │     │  SQLite         │
└─────────────────┘     └──────────────────────┘     └─────────────────┘
```

**Flujo completo:**

```
CoinGecko API ──┐
                ├──▶ extract_prices() ──▶ transform_prices() ──▶ load_prices() ──▶ SQLite DB
DolarAPI ───────┘
```

> **¿Por qué separar en 3 fases?**
> Si mañana cambias la API de precios, solo tocas `extract.py`. Si migras de SQLite a PostgreSQL, solo tocas `load.py`. El resto del pipeline no se entera. Eso es **desacoplamiento real**.

---

## 📂 Estructura del Proyecto

```
crypto-price-pipeline/
│
├── 📁 pipelines/
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
├── run_crypto.py             # Orquestador del pipeline
├── .env                      # ⚠️ Credenciales (NO se sube a git)
├── .env.example              # Plantilla de variables de entorno
├── requirements.txt          # Dependencias del proyecto
└── README.md
```

---

## 🔌 Detalle de cada módulo

| Archivo | Función | Responsabilidad |
|---|---|---|
| `pipelines/crypto/extract.py` | `extract_prices()` | Llama a CoinGecko y DolarAPI, retorna `dict` con precios |
| `pipelines/crypto/transform.py` | `transform_prices()` | Convierte el `dict` en lista de tuplas `(coin, price, timestamp)` |
| `pipelines/crypto/load.py` | `load_prices()` | Inserta cada registro en SQLite usando las funciones de `db/sqlite.py` |
| `db/sqlite.py` | Funciones puras | `get_connection`, `create_tables`, `get_or_create_coin`, `insert_price_log` |
| `config/crypto_config.py` | Config | Carga `COINGECKO_API_KEY` desde `.env` via `python-dotenv` |
| `run_crypto.py` | Orquestador | Llama ETL en orden: crea tablas → extrae → transforma → carga |

---

## 🗄️ Base de Datos — Diseño Normalizado

La DB está **normalizada** para evitar redundancia y garantizar integridad referencial:

```
┌──────────────────┐          ┌────────────────────────┐
│      coins       │          │       price_logs        │
├──────────────────┤          ├────────────────────────┤
│ id (PK) 🔑       │◄────┐    │ id (PK) 🔑              │
│ name (UNIQUE)    │     └────│ coin_id (FK) 🔗         │
└──────────────────┘          │ price (REAL)            │
                              │ captured_at (TEXT)      │
                              └────────────────────────┘
```

**¿Por qué esta estructura?**

- `coins` es la **tabla maestra** — cada moneda se registra **una sola vez**, sin importar cuántos precios se capturen.
- `price_logs` guarda el **histórico** con una fila por moneda por captura.
- La **Foreign Key** garantiza integridad referencial: no puede existir un precio sin su moneda.
- `get_or_create_coin()` registra automáticamente monedas nuevas si CoinGecko cambia su lista.

**Crecimiento esperado:**

> 21 activos × 24 capturas/día × 7 días = **3,528 registros** — perfectamente manejable en SQLite.

---

## 🛠️ Tecnologías

| Categoría | Tecnología | Uso |
|---|---|---|
| **Lenguaje** | Python 3.9+ | Todo el proyecto |
| **Base de datos** | SQLite | Histórico de precios, sin servidor requerido |
| **API precios** | CoinGecko | Top 20 criptomonedas por market cap en USD |
| **API cambio** | DolarAPI | Tipo de cambio USD/COP en tiempo real |
| **Data** | Pandas | Análisis y consultas del histórico |
| **HTTP** | Requests | Llamadas a las APIs externas |
| **Seguridad** | python-dotenv | Gestión segura de credenciales |

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/mcdatax/crypto-price-pipeline.git
cd crypto-price-pipeline
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

```bash
cp .env.example .env
```

Edita el archivo `.env` con tu API key de CoinGecko:

```env
# .env — NUNCA subas este archivo a git
COINGECKO_API_KEY=tu_api_key_aqui
```

> Puedes obtener una API key gratis en [coingecko.com/api](https://www.coingecko.com/api/documentation).
> El archivo `.env` ya está en `.gitignore`. Nunca lo subas a un repositorio público.

---

## 💻 Uso

### Ejecución manual

```bash
python run_crypto.py
```

Salida esperada:

```
Tablas listas en: crypto_prices.db
Iniciando pipeline de criptomonedas...
Obteniendo datos de CoinGecko...
Datos obtenidos exitosamente.
Procesando y almacenando datos en la DB...
Datos cargados exitosamente en: crypto_prices.db
```

### Automatizar cada hora con `cron` (macOS/Linux)

```bash
crontab -e
```

Añadir esta línea (ajusta la ruta a tu proyecto):

```
0 * * * * cd /ruta/al/proyecto && .venv/bin/python run_crypto.py
```

### Consultar el histórico con pandas

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect("crypto_prices.db")

# Ver todos los precios de Bitcoin
df = pd.read_sql(
    "SELECT p.captured_at, p.price "
    "FROM price_logs p "
    "JOIN coins c ON c.id = p.coin_id "
    "WHERE c.name = 'Bitcoin' "
    "ORDER BY p.captured_at",
    conn
)

conn.close()
print(df)
```

```python
# Ver el precio más reciente de todas las monedas
df = pd.read_sql(
    "SELECT c.name, p.price, p.captured_at "
    "FROM price_logs p "
    "JOIN coins c ON c.id = p.coin_id "
    "WHERE p.captured_at = (SELECT MAX(captured_at) FROM price_logs) "
    "ORDER BY p.price DESC",
    conn
)
```

---

## ✅ Buenas Prácticas aplicadas

Este proyecto fue construido siguiendo los estándares reales de la industria de **Data Engineering**:

- **📦 Separación por módulos** — cada archivo tiene una única responsabilidad (principio SRP)
- **🔒 Credenciales en `.env`** — ninguna API key hardcodeada en el código
- **🗂️ Imports absolutos** — `from db.sqlite import ...` siempre desde la raíz del proyecto
- **🧩 Funciones puras** — sin efectos secundarios ocultos, fáciles de testear de forma aislada
- **🔗 DB normalizada** — sin redundancia, con Foreign Keys e integridad referencial
- **⚛️ Transacciones atómicas** — `commit()` va después de todas las inserciones, no dentro del loop
- **🛡️ SQL parametrizado** — uso de `?` en lugar de f-strings, previniendo SQL injection
- **📝 Type hints** — `def load_prices(data: list, db_path: str) -> None`
- **📋 Docstrings** — cada función documenta qué recibe, qué hace y qué retorna
- **🏷️ `if __name__ == "__main__"`** — los scripts son ejecutables e importables sin efectos secundarios

---

## 📦 Dependencias

```
requests==2.32.5          # Llamadas HTTP a las APIs (CoinGecko, DolarAPI)
python-dotenv==1.2.1      # Carga segura de credenciales desde .env
pandas==2.3.3             # Análisis y procesamiento del histórico de precios
```

---

## 🗺️ Roadmap

- [x] Pipeline Crypto con histórico en SQLite normalizada
- [x] Arquitectura ETL modular por capas
- [x] Gestión segura de credenciales con `.env`
- [ ] Scheduler automático con APScheduler
- [ ] Logging estructurado (reemplazar `print()` por `logging`)
- [ ] Tests unitarios con `pytest`
- [ ] Dashboard de análisis con pandas + matplotlib
- [ ] Migración a PostgreSQL para mayor escala
- [ ] Despliegue en AWS Lambda / Azure Functions

---

## 👤 Autor

**mcdatax**

[![GitHub](https://img.shields.io/badge/GitHub-mcdatax-181717?logo=github)](https://github.com/mcdatax)

---

<div align="center">

**⭐ Si te resulta útil, dale una estrella al repositorio ⭐**

[🐛 Reportar Bug](https://github.com/mcdatax/crypto-price-pipeline/issues) • [💡 Solicitar Feature](https://github.com/mcdatax/crypto-price-pipeline/issues)

</div>
