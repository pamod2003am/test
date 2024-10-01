from pyrogram import Client, filters 
from typing import Union, Optional
from pyrogram.types import Message
from .WaClient import StartWaClient
from .Config import TOKEN , API_ID , API_HASH
import asyncio
from threading import Thread
import subprocess
from flask import Flask
from .health import app
import os

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
        
    # async def pass_health_check(self):
    #     def run_flask():
    #         os.system("gunicorn -w 1 -b 0.0.0.0:8443 Bot.health:app --threads 2")
    #     self.flask_thread = Thread(target=run_flask)
    #     self.flask_thread.start()

    async def pass_health_check(self):
        def run_flask():
            self.flask_process = subprocess.Popen(
                ["gunicorn", "-w", "1", "-b", "0.0.0.0:8443", "Bot.health:app", "--threads", "2"]
            )
        
        # Start Flask in a new thread
        flask_thread = Thread(target=run_flask)
        flask_thread.start()

        # Wait for 10 seconds
        await asyncio.sleep(10)

        # Terminate the Gunicorn process
        if self.flask_process:
            self.flask_process.terminate()  # Gracefully terminate the process
            self.flask_process.wait()  # Wait for the process to terminate
            print("Flask app stopped.")
        
    async def stop(self, *args):
        print(f"{self._bot.first_name} - @{self._bot.username} Stoped")
        await super().stop()

_Bot().run()
