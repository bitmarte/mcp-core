from fastmcp import FastMCP
from .config import CoreConfig
from .helpers.logger import LoggerHelper
from .helpers.sqlite import SQLiteHelper
from .helpers.parquet import ParquetHelper

class CoreAPI:
    """Oggetto centrale da passare ai tool con tutti gli helper disponibili."""

    def __init__(self):
        # CoreConfiguration and Logging
        self.config = CoreConfig()
        self.logger = LoggerHelper(self.config)

        # Helper configurations
        self.sqlite = SQLiteHelper(self.config)
        self.parquet = ParquetHelper(self.config)

        # Istanza MCP principale, così i tools possono usare l'annotation @core_api.mcp.tool
        self.mcp = FastMCP(name=self.config.instance_name)

        self._log_startup_info()

    def _log_startup_info(self):
        self.logger.info("=== CoreAPI Startup ===")
        self.logger.info(f"Core variables: {self.config.core}")
        self.logger.info(f"SQLite aliases: {list(self.config.sqlite.keys())}")
        self.logger.info(f"Parquet aliases: {list(self.config.parquet.keys())}")
        self.logger.info("=======================")

# Istanza globale già pronta per i tools
core_api = CoreAPI()
