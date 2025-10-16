import sqlite3
import pandas as pd
from pathlib import Path
from mcp_core.helpers.logger import LoggerHelper

class SQLiteHelper:
    """Helper per più database SQLite, accessibili tramite alias,
    con output coerente in DataFrame pandas e logging centralizzato."""

    def __init__(self, config):
        """
        config: CoreConfig
        """
        self.config = config
        self.db_paths = config.sqlite
        self.logger = LoggerHelper(config)

    def _get_db_path(self, alias: str) -> Path:
        path = self.db_paths.get(alias)
        if not path:
            raise ValueError(f"Alias SQLite '{alias}' non trovato.")
        path = Path(path)
        if not path.exists():
            self.logger.warning(f"File DB SQLite '{path}' non esiste ancora.")
        return path

    def query(self, sql: str, params: tuple | None = None, alias: str = "default"):
        """Esegue una query SQL e ritorna raw results (lista di tuple)."""
        params = params or ()
        db_path = self._get_db_path(alias)
        self.logger.debug(f"Eseguo query SQLite su '{alias}': {sql} | params={params}")
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            return cursor.fetchall()

    def query_df(self, sql: str, params: tuple | None = None, alias: str = "default") -> pd.DataFrame:
        """Esegue una query SQL e ritorna un DataFrame pandas."""
        params = params or ()
        db_path = self._get_db_path(alias)
        self.logger.debug(f"Eseguo query_df SQLite su '{alias}': {sql} | params={params}")
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql_query(sql, conn, params=params)
        return df

    def execute(self, sql: str, params: tuple | None = None, alias: str = "default"):
        """Esegue query di modifica (INSERT, UPDATE, DELETE) e committa."""
        params = params or ()
        db_path = self._get_db_path(alias)
        self.logger.debug(f"Eseguo execute SQLite su '{alias}': {sql} | params={params}")
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
