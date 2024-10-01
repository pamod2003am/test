from pyrogram import Client, filters
from pyrogram.types import Message
from .verify import verify_whatsapp
from ..Database import userDB

@Client.on_message(filters.command("start"))
@userDB
async def start_command(client: Client, message: Message):
    await message.delete()
    commands = message.command
    param = commands[-1] if len(message.command) != 1 else None
    if not param:
        await message.reply_text("Hello! I'm your bot, ready to assist you.")
    else:await handle_start_param(client, message, param)


async def handle_start_param(client: Client, message: Message, param: str):
    if param.startswith('VERIFY_'):
        encypt_number = param.replace('VERIFY_','')
        await verify_whatsapp(client,message,encypt_number)