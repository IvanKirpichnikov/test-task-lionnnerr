import asyncio
import logging

from app.main import run

logging.basicConfig(level=logging.DEBUG)
asyncio.run(run())
