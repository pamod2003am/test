from pyrogram import Client
from .client import WAClient
import asyncio

WaBot = None
async def StartWaClient(bot: Client = None):
    global WaBot
    if WaBot:return WaBot
    else:
        WaBot = WAClient(bot)
        asyncio.create_task(WaBot.polling())
        await asyncio.sleep(2)
        return WaBot
    
