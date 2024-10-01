from pyrogram import Client, filters
from pyrogram.types import Message
import os
import sys

@Client.on_message(filters.command("restart"))
async def start_command(client: Client, message: Message):
    await message.delete()
    os.execl(sys.executable, sys.executable, "-m", "Bot", *sys.argv[1:])



