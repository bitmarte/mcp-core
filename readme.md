# MCP Core

**MCP Core** è il cuore modulare di un framework MCP (Modular Control Platform) in Python, progettato per eseguire un server FastMCP con supporto per strumenti (tools) estendibili tramite decoratori.  
Permette di centralizzare la logica, la configurazione, il logging e l'accesso ai database, lasciando ai tools il compito di implementare funzionalità specifiche.

## Struttura del progetto

```
./
├── .gitignore
├── pyproject.toml
├── readme.md
└── src/
    └── mcp_core/
        ├── __init__.py
        ├── cli.py
        ├── config.py
        ├── core.py
        ├── helpers/
        │   ├── logger.py
        │   ├── parquet.py
        │   └── sqlite.py
        ├── loader.py
        └── server.py
```

## Funzionamento

### CoreAPI

`CoreAPI` è l’oggetto centrale del progetto, contiene:

- `config`: configurazioni principali (host, port, path, protocolli, ecc.)
- `logger`: logger centralizzato tramite `LoggerHelper`
- `mcp`: istanza di `FastMCP` per registrare e eseguire i tools

Tutti i tools possono accedere al `core_api` globale tramite:

```python
from mcp_core.core import core_api
```

### Tools

I tools sono moduli Python collocati in una cartella tools/. Ogni funzione che deve essere registrata come tool viene decorata con:

```python
@core_api.mcp.tool
def health_check() -> dict:
    return {"status": "ok"}
```

Il loader importa automaticamente tutti i moduli presenti nella cartella tools (anche ricorsivamente) e registra le funzioni decorate.
Non è necessario esportare o restituire esplicitamente le funzioni dal loader.

### Loader

`loader.py` si occupa di:

- Importare dinamicamente tutti i moduli Python dalla cartella dei tools
- Gestire sia percorsi fisici (/app/tools) sia package Python (tools)
- Registrare automaticamente i tools decorati con @core_api.mcp.tool

Esempio di utilizzo:

```python
from mcp_core.loader import load_tools

tools = load_tools("/app/tools")  # o "tools" se è un package Python
```

### Server

`server.py` gestisce l’avvio del server MCP. Può ricevere:

- host, port, path della connessione
- tools caricati dal loader
- start_callback opzionale per eseguire logiche personalizzate all’avvio

### CLI

`cli.py` è l’entry point principale per avviare il server.
Funzionalità principali:

- Legge le configurazioni da CoreConfig
- Carica i tools tramite load_tools
- Istanzia FastMCP con i tools caricati
- Avvia il server MCP con callback personalizzato

### Helpers

Da intendersi come plugins di supporto per integrare fonti date varie oppure utilità (al momento non suddivise per competenza, da valutare poi strada facendo).
Attualmente abbiamo:

- `logger.py`: wrapper per logging centralizzato (LoggerHelper)
- `sqlite.py`: helper per gestire più database SQLite, query e DataFrame Pandas
- `parquet.py`: helper per leggere e scrivere file Parquet

### Configurazione

Le configurazioni principali vengono lette da CoreConfig e includono:

- instance_name: nome del server
- host, port, path: endpoint di ascolto
- protocol: tipo di trasporto (http)
- log_level: livello di logging

Esempio di utilizzo:

```python
from mcp_core.core import core_api

logger = core_api.logger
config = core_api.config

logger.info(f"Server '{config.core.get('instance_name')}' pronto all'avvio")
```

## Avvio del server

Tramite script `start.sh` è possibile passare parametri aggiuntivi che andranno al `podman run` (es. volumi, variabili, ...).
Nel container, i tools vengono montati in /app/tools e caricati automaticamente.

## Note

- I tools devono usare l’istanza globale core_api e il decoratore @core_api.mcp.tool.
- Non è necessario avere file `__init__`.py nelle sottocartelle dei tools grazie al loader dinamico.
- Tutti i log e le eccezioni durante il caricamento dei tools vengono riportati tramite LoggerHelper.

## Contributi per i tools di default

Per aggiungere un nuovo tool:

- Creare un modulo Python in tools/
- Definire una funzione decorata con @core_api.mcp.tool
- Il loader importerà automaticamente il modulo e registrerà la funzione come tool eseguibile

Esempio di utilizzo:

```python
# tools/default/health_check.py
from mcp_core.core import core_api

@core_api.mcp.tool
def health_check() -> dict:
    core_api.logger.info("Eseguo health_check")
    return {"status": "ok"}
```