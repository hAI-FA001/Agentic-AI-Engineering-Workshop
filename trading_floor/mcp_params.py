import os
from dotenv import load_dotenv


load_dotenv(override=True)

# I'm using Google Custom Search instead of Brave API
search_env = {"GOOGLE_API_KEY": os.environ['GOOGLE_API_KEY'], "GOOGLE_SEARCH_ENGINE_ID": os.environ['GOOGLE_SEARCH_ENGINE_ID']}
polygon_api_key = os.environ['POLYGON_API_KEY']


# assume we have neither realtime nor paid Polygon.io (check workshop's GitHub for what value to use for the market_mcp variable)
market_mcp = {"command": "uv", "args": ["run", "market_server.py"]}

trader_mcp_server_params = [
    {"command": "uv", "args": ["run", "accounts_server.py"]},
    # workshop also uses push_server.py for Push notifications
    market_mcp,
]

def researcher_mcp_server_params(name: str):
    return [
        {"command": "uvx", "args": ["mcp-server-fetch"]},
        # I'm using Google Custom Search instead of Brave API
        {
            "command": "node",
            "args": [f"{os.getcwd()}/mcp-google-custom-search-server/build/index.js"],
            "env": search_env,
         },
        {"command": "npx", "args": ["-y", "mcp-memory-libsql"], "env": {"LIBSQL_URL": f"file:./memory/{name}.db"}}
    ]