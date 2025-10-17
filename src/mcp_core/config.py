import os
from pathlib import Path
from dotenv import load_dotenv

# Carica il file .env
def _load_env():
    # cerca in /app/.env o nel package installato
    paths = [
        Path("/app/.env"),
        Path(__file__).parent / ".env",
        Path.cwd() / ".env",
    ]
    for p in paths:
        if p.exists():
            print(f"[DEBUG] Loading env from: {p}")
            load_dotenv(p, override=True)
            print(f"[DEBUG] CORE_PORT after load: {os.getenv('CORE_PORT')}")
            break
    else:
        print("[DEBUG] No .env found")

_load_env()

class CoreConfig:
    """Configurazioni centralizzate per tutti gli helper,
    supporta più DB e più root Parquet con alias,
    con lettura ibrida da .env + variabili d'ambiente."""

    def __init__(self, reload_env: bool = True):
        if reload_env:
            _load_env()  # <-- forza ricaricamento anche se già caricato
        # Loader generico CORE_ per tutte le configurazioni
        self.core = self._load_core_configs()

        # Loader specifici per helpers
        self.sqlite = self._load_sqlite_configs()
        self.parquet = self._load_parquet_configs()

    @classmethod
    def from_env(cls):
        """Crea istanza di CoreConfig caricando .env + variabili ambiente."""
        return cls()

    # --- Proprietà di accesso rapido per le configurazioni principali ---
    @property
    def instance_name(self):
        return self.core.get("instance_name", "MCP Server")

    @property
    def host(self):
        return self.core.get("host", "0.0.0.0")

    @property
    def port(self):
        return int(self.core.get("port", 8100))

    @property
    def path(self):
        return self.core.get("path", "/mcp")

    @property
    def log_level(self):
        return self.core.get("log_level", "INFO")

    # --- Loader interni ---
    def _load_core_configs(self):
        """Legge tutte le variabili d'ambiente che iniziano con CORE_"""
        result = {}
        for key, value in os.environ.items():
            if key.startswith("CORE_"):
                config_key = key[len("CORE_"):].lower()
                result[config_key] = value
        return result

    def _load_sqlite_configs(self):
        """Legge variabili d'ambiente SQLITE_DB_URL_<ALIAS> e ritorna {alias: path}"""
        result = {}
        for key, value in os.environ.items():
            if key.startswith("SQLITE_DB_URL_"):
                alias = key[len("SQLITE_DB_URL_"):].lower()
                result[alias] = value
        if not result:
            result["default"] = "data/db.sqlite"
        return result

    def _load_parquet_configs(self):
        """Legge variabili d'ambiente PARQUET_FILES_ROOT_<ALIAS> e ritorna {alias: folder}"""
        result = {}
        for key, value in os.environ.items():
            if key.startswith("PARQUET_FILES_ROOT_"):
                alias = key[len("PARQUET_FILES_ROOT_"):].lower()
                result[alias] = value
        if not result:
            result["default"] = "data/parquet/"
        return result
