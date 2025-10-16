import sys
import os
from fastmcp import FastMCP
from mcp_core.core import core_api
from mcp_core.loader import load_tools
from mcp_core.server import run_server

def main():
    logger = core_api.logger
    config = core_api.config

    instance_name = config.core.get("instance_name", "My First MCP Server")
    logger.info(f"Avvio MCP server '{instance_name}'")

    # Determina il percorso fisico dei tools in container
    tools_path = "/app/tools" if os.path.isdir("/app/tools") else "tools"

    # Importa tutti i moduli dei tools (il decoratore registra le funzioni)
    load_tools(tools_path)

    # Espone l'FastMCP inizializzata nel core in modo che ce ne sia soltanto una
    mcp = core_api.mcp

    # Callback che avvia il server MCP
    def start_server(host, port, path, _):
        transport = config.core.get("protocol", "http")
        logger.info(f"Avvio FastMCP su {transport}://{host}:{port}{path}")
        mcp.run(transport=transport, host=host, port=port, path=path)

    # Esegue l’avvio passando il callback
    run_server(start_callback=start_server)

if __name__ == "__main__":
    sys.exit(main())
