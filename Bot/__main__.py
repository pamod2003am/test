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
        # await asyncio.create_task(self.pass_health_check())
        
    async def pass_health_check(self):
        # self.flask_process = subprocess.Popen(
        #         ["python", "Bot/health.py", "run", "--host=0.0.0.0", "--port=8443"]
        #     )
        def run_flask():
            os.system("gunicorn -w 1 -b 0.0.0.0:8443 Bot.health:app --threads 2")
            # app.run(host="0.0.0.0", port=8443, use_reloader=False)

        self.flask_thread = Thread(target=run_flask)
        self.flask_thread.start()
        # thread = Thread(target=run_gunicorn)
        # Start Flask app in a new thread
        # thread = Thread(target=lambda: app.run(host="0.0.0.0", port=8443, use_reloader=False))
        # thread.daemon = True  # Daemon thread to ensure it exits with the program
        # thread.start()

    async def stop(self, *args):
        print(f"{self._bot.first_name} - @{self._bot.username} Stoped")
        await super().stop()

_Bot().run()
