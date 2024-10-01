from pyrogram import Client, filters 
from typing import Union, Optional
from pyrogram.types import Message
from .WaClient import StartWaClient
from .Config import TOKEN , API_ID , API_HASH
import subprocess
import asyncio
import os
from flask import Flask

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return "OK", 200


class _Bot(Client):
    def __init__(self):
        super().__init__(
            name="Uploader-X",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=TOKEN,
            plugins=dict(root="Bot.Plugins"),
            workers=200,
        )
        self.wabot = None 
    async def start(self):
        self.wabot = await StartWaClient(self)
        setattr(self, 'wabot', self.wabot)
        await super().start()
        self._bot = await self.get_me()
        print(f"{self._bot.first_name} - @{self._bot.username} Started")
        await asyncio.create_task(self.pass_health_check())
        
    async def pass_health_check(self):
        # subprocess.Popen(["node", "Bot/WaClient/health.js"])
        app.run(port=8443)

    async def stop(self, *args):
        print(f"{self._bot.first_name} - @{self._bot.username} Stoped")
        await super().stop()

_Bot().run()

