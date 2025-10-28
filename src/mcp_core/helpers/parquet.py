from pathlib import Path
import duckdb
from mcp_core.helpers.logger import LoggerHelper

class ParquetHelper:
    """Helper per eseguire query SQL direttamente su file Parquet,
    con alias gestiti da CoreConfig e logging centralizzato."""

    def __init__(self, config):
        self.config = config
        self.roots = config.parquet
        self.logger = LoggerHelper(config)

    def get_path(self, alias: str):
        path = self.roots.get(alias)
        return path

    def query(self, sql: str):
        self.logger.debug(f"Eseguo query DuckDB:\n{sql}")
        con = duckdb.connect(database=':memory:')
        df = con.execute(sql).fetchdf()
        return df
