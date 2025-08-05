from mcp.server.fastmcp import FastMCP
from accounts import Account

mcp = FastMCP('accounts_server')

@mcp.tool()
async def get_balance(name: str) -> float:
    """Get the cash balance of the given account name"""
    return Account.get(name).balance

@mcp.tool()
async def get_holdings(name: str) -> float:
    """Get the holdings of the given account name"""
    return Account.get(name).holdings

@mcp.tool()
async def buy_shares(name: str, symbol: str, quantity: int, rationale: str) -> float:
    """Buy shares of a stock.
    Args:
        name: name of the account holder
        symbol: symbol of the stock
        quantity: how many shares to buy
        rationale: reason for purchasing, fit with the account's strategy"""
    return Account.get(name).buy_shares(symbol, quantity, rationale)

@mcp.tool()
async def sell_shares(name: str, symbol: str, quantity: int, rationale: str) -> float:
    """Sell shares of a stock.
    Args:
        name: name of the account holder
        symbol: symbol of the stock
        quantity: how many shares to sell
        rationale: reason for selling, fit with the account's strategy"""
    return Account.get(name).sell_shares(symbol, quantity, rationale)

@mcp.tool()
async def change_strategy(name: str, strategy: str) -> str:
    """At your discretion, call this to change your investment strategy"""
    return Account.get(name).change_strategy(strategy)

