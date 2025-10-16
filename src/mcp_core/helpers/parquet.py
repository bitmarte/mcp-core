from pathlib import Path
import duckdb
from mcp_core.helpers.logger import LoggerHelper

class ParquetHelper:
    """Helper per eseguire query SQL direttamente su file Parquet,
    con alias gestiti da CoreConfig e logging centralizzato."""

    def __init__(self, config):
        """
        config: CoreConfig
        """
        self.config = config
        self.roots = config.parquet
        self.logger = LoggerHelper(config)

    def query(self, sql: str, alias: str):
        """
        Esegue una query SQL sull'alias, con il quale il CoreConfig recupera la root_path dove stanno tutti i parquet files
        """
        sql_to_execute = sql
        root = self.roots.get(alias)

        sql_to_execute = sql.replace(f"read_parquet('{alias}'", f"read_parquet('{root}'")

        self.logger.debug(f"Eseguo query DuckDB:\n{sql_to_execute}")
        con = duckdb.connect(database=':memory:')
        df = con.execute(sql_to_execute).fetchdf()
        return df
