from agents import add_trace_processor

from tracers import LogTracer
from market import is_market_open
from traders import Trader

from typing import List
import asyncio
from dotenv import load_dotenv
import os

load_dotenv(override=True)

RUN_EVERY_N_MINUTES = 1
RUN_EVEN_WHEN_MARKET_IS_CLOSED = os.getenv('RUN_EVEN_WHEN_MARKET_IS_CLOSED', 'false').strip().lower() == 'true'

names = ['Warren', 'George', 'Ray', "Cathie"]
lastnames = ['Patience', 'Bold', 'Systematic', 'Crypto']

model_names = ['gemini-2.5-flash-lite']*4
short_model_names = ['Gemini 2.5 Flash']*4

def create_traders() -> List[Trader]:
    traders = []
    for name, lastname, model_name in zip(names, lastnames, model_names):
        traders.append(Trader(name, lastname, model_name))
    return traders

async def run_every_n_mins():
    add_trace_processor(LogTracer())
    traders = create_traders()

    while True:
        if RUN_EVEN_WHEN_MARKET_IS_CLOSED or is_market_open():
            await asyncio.gather(*[trader.run() for trader in traders])
        else:
            print('Market is closed, skipping run')
        
        await asyncio.sleep(RUN_EVERY_N_MINUTES*60)

if __name__ == "__main__":
    print(f'Starting scheduler to run every {RUN_EVERY_N_MINUTES} mins')
    asyncio.run(run_every_n_mins())
