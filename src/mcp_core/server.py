# src/mcp_core/server.py
from mcp_core.core import core_api

def run_server(tools: list = None, start_callback=None):
    """
    Avvia il server MCP tramite il callback passato.
    Permette di caricare i tools e lasciare l'istanza FastMCP al cli.py.
    """
    logger = core_api.logger
    config = core_api.config
    instance_name = config.core.get("instance_name", "MCP server")

    if tools:
        logger.info(f"{len(tools)} tools registrati nel server")

    if callable(start_callback):
        try:
            host = config.core.get("host", "0.0.0.0")
            port = int(config.core.get("port", 8000))
            path = config.core.get("path", "/mcp")
            start_callback(host, port, path, tools)
        except Exception as e:
            logger.error(f"Errore durante l'avvio del server MCP: {e}", exc_info=True)
    else:
        logger.error("Nessun callback valido per avviare il server MCP")
