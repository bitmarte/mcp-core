import logging
import sys

class LoggerHelper:
    """Logger centralizzato per core e tool"""

    _cache = {}

    def __init__(self, config, name=None):
        self.config = config
        self.name = name or config.core.get("instance_name", "MCP")
        cache_key = self.name.lower()

        level_str = config.core.get("log_level", "INFO").upper()
        level_value = getattr(logging, level_str, logging.INFO)

        if cache_key in LoggerHelper._cache:
            self.logger = LoggerHelper._cache[cache_key]
            # Se il livello nel .env è cambiato, aggiorna il logger
            if self.logger.level != level_value:
                self.logger.setLevel(level_value)
                self.logger.debug(f"[LoggerHelper] Log level aggiornato a {level_str}")
        else:
            self.logger = logging.getLogger(self.name)
            self.logger.setLevel(level_value)

            if not self.logger.handlers:
                handler = logging.StreamHandler(sys.stdout)
                formatter = logging.Formatter(
                    "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
                )
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)

            LoggerHelper._cache[cache_key] = self.logger

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)
