from agents import Agent, Tool, Runner, OpenAIChatCompletionsModel, trace, AsyncOpenAI
from agents.mcp import MCPServerStdio

from contextlib import AsyncExitStack
from dotenv import load_dotenv
import os
import json

from accounts_client import read_accounts_resource, read_strategy_resource
from tracers import make_trace_id
from templates import researcher_instructions, trader_instructions, trade_message, rebalance_message, research_tool
from mcp_params import trader_mcp_server_params, researcher_mcp_server_params

load_dotenv(override=True)

gemini_api_key = os.environ['GEMINI_API_KEY']
google_api_key = os.environ['GOOGLE_API_KEY']
GEMINI_BASE_URL = os.environ['GEMINI_BASE_URL']

MAX_TURNS = 30

gemini_client = AsyncOpenAI(base_url=GEMINI_BASE_URL, api_key=gemini_api_key)

def get_model(model_name: str):
    return OpenAIChatCompletionsModel('gemini-2.5-flash', gemini_client)

async def get_researcher(mcp_servers, model_name) -> Agent:
    return Agent(
        name='Researcher',
        instructions=researcher_instructions(),
        model=get_model(model_name),
        mcp_servers=mcp_servers
    )

async def get_researcher_tool(mcp_servers, model_name) -> Tool:
    researcher = await get_researcher(mcp_servers, model_name)
    return researcher.as_tool(tool_name='Researcher', tool_description=research_tool())

class Trader:
    def __init__(self, name: str, lastname='Trader', model_name='gemini-2.5-flash'):
        self.name = name
        self.lastname = lastname
        self.agent = None
        self.model_name = model_name
        self.do_trade = True
    
    async def create_agent(self, trader_mcp_servers, researcher_mcp_servers) -> Agent:
        tool = await get_researcher_tool(researcher_mcp_servers, self.model_name)
        
        self.agent = Agent(
            name=self.name,
            instructions=trader_instructions(self.name),
            model=get_model(self.model_name),
            tools=[tool],
            mcp_servers=trader_mcp_servers,
        )
        
        return self.agent
    
    async def get_account_report(self) -> str:
        account = await read_accounts_resource(self.name)
        account_json = json.loads(account)
        account_json.pop('portfolio_value_time_series', None)
        return json.dumps(account_json)
    
    async def run_agent(self, trader_mcp_servers, researcher_mcp_servers):
        self.agent = await self.create_agent(trader_mcp_servers, researcher_mcp_servers)
        
        account = await self.get_account_report()
        strategy = await read_strategy_resource(self.name)
        
        message = trade_message(self.name, strategy, account) if self.do_trade else rebalance_message(self.name, strategy, account)

        await Runner.run(self.agent, message, max_turns=MAX_TURNS)
    
    async def run_with_mcp_servers(self):
        async with AsyncExitStack() as stack:
            trader_mcp_servers = [await stack.enter_async_context(MCPServerStdio(params, client_session_timeout_seconds=120)) for params in trader_mcp_server_params]
            async with AsyncExitStack() as stack:
                researcher_mcp_servers = [await stack.enter_async_context(MCPServerStdio(params, client_session_timeout_seconds=120)) for params in researcher_mcp_server_params(self.name)]
                await self.run_agent(trader_mcp_servers, researcher_mcp_servers)
    
    async def run_with_trace(self):
        trace_name = f'{self.name}-trading' if self.do_trade else f'{self.name}-rebalancing'
        trace_id = make_trace_id(self.name.lower())

        with trace(trace_name, trace_id=trace_id):
            await self.run_with_mcp_servers()
    
    async def run(self):
        try:
            await self.run_with_trace()
        except Exception as e:
            print(f'Error running Trader "{self.name}": {e}')
        self.do_trade = not self.do_trade