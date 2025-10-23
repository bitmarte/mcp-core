import os
import sys
import importlib
from mcp_core.core import core_api

APP_DIR = "/app"
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

def load_tools(tools_path: str = "tools") -> list[str]:
    """
    Importa tutti i moduli Python nella cartella tools.
    Il decoratore @core_api.mcp.tool registra automaticamente le funzioni in FastMCP.
    """
    imported_modules = []

    # Determina la directory fisica dei tools
    if os.path.isdir(tools_path):
        base_dir = tools_path
        package_prefix = os.path.basename(tools_path)
    else:
        try:
            module = importlib.import_module(tools_path)
            base_dir = os.path.dirname(module.__file__) or os.path.join(APP_DIR, tools_path)
            package_prefix = tools_path
        except ModuleNotFoundError:
            core_api.logger.warning(f"Cartella o package '{tools_path}' non trovata.")
            return imported_modules

    # Aggiunge la cartella al sys.path se necessario
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)

    # Importa ricorsivamente tutti i moduli .py
    for root, _, files in os.walk(base_dir):
        # Escludi tutte le cartelle chiamate "examples"
        dirs[:] = [d for d in dirs if d != "examples"]

        for filename in files:
            if not filename.endswith(".py") or filename.startswith("_"):
                continue

            rel_path = os.path.relpath(root, base_dir).replace(os.sep, ".")
            module_name = filename[:-3]
            full_module_name = (
                f"{package_prefix}.{rel_path}.{module_name}" if rel_path != "." else f"{package_prefix}.{module_name}"
            )

            try:
                importlib.import_module(full_module_name)
                imported_modules.append(full_module_name)
                core_api.logger.info(f"Modulo tool '{full_module_name}' importato correttamente.")
            except Exception as e:
                core_api.logger.error(f"Errore importando '{full_module_name}': {e}")

    if not imported_modules:
        core_api.logger.warning(f"Nessun modulo tool trovato in '{tools_path}'")

    core_api.logger.info(f"Tutti i moduli tools importati: {imported_modules}")
    return imported_modules
