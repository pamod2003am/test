from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from ..WaClient import StartWaClient
from ..Database import UserDB
from ..Config import WHATSAPP_GROUP , WHATSAPP_GROUP_LINK, progress_fill ,progress_pending 
import asyncio
import os
import time
import math


@Client.on_message(filters.document)
async def handle_documents(client: Client, message: Message):
    if message.document.file_size < 80*1024*1024:
        asyncio.create_task(download_and_upload(client,message))
    else:
        await message.reply('Currently we only upload files less than 80mb')

async def download_and_upload(client: Client, message:Message):
    dm = None
    start_time = time.time()
    # async def progress_callback(current, total):
    #     await dm.edit_text(f"Downloading: {current * 100 / total:.1f}%")
    
    async def progress_callback(current, total):
        # Calculate percentage
        try:
            percentage = current * 100 / total

            # Calculate download speed (bytes per second)
            elapsed_time = time.time() - start_time
            speed = current / elapsed_time if elapsed_time > 0 else 0

            # Convert speed to human-readable format (KB/s or MB/s)
            if speed > 1024 * 1024:
                speed_str = f"{speed / (1024 * 1024):.2f} MB/s"
            else:
                speed_str = f"{speed / 1024:.2f} KB/s"

            # Calculate ETA
            eta = (total - current) / speed if speed > 0 else 0
            eta_str = time.strftime("%H:%M:%S", time.gmtime(eta))
            progress = f"""{"".join([progress_fill for i in range(math.floor(percentage / 7))])}{"".join([progress_pending for i in range(14 - math.floor(percentage / 7))])} """
            # Send the update message
            await dm.edit_text(
                f"┌ <b><i>Downloading</i></b>\n"
                f"├ {progress}\n"
                f"├ <b><i>Percentage</i></b> : <code>{percentage:.1f}%</code>\n"
                f"├ <b><i>Current</i></b> : <code>{current / (1024 * 1024):.2f} MB</code>\n"
                f"├ <b><i>Total</i></b> : <code>{total / (1024 * 1024):.2f} MB</code>\n"
                f"├ <b><i>Speed</i></b> : <code>{speed_str}</code>\n"
                f"├ <b><i>Time elapsed</i></b> : <code>{time.strftime('%H:%M:%S', time.gmtime(elapsed_time))}</code>\n"
                f"└ <b><i>ETA</i></b> : <code>{eta_str}</code>"
            ,parse_mode=ParseMode.HTML)
        except Exception as e:print(e)

    wabot = await StartWaClient()
    dm = await message.reply('Preparing ...',quote=True)
    # client.set_parse_mode(ParseMode.HTML)
    file = await client.download_media(message=message,file_name=message.document.file_name,progress=progress_callback)
    await dm.edit_text('Download finished')
    await asyncio.sleep(1)
    await dm.edit_text('Uploading...')
    whatsapp_id = UserDB().get_whatsapp_id(user_id=message.from_user.id)
    if not whatsapp_id:
        whatsapp_id = WHATSAPP_GROUP
        await message.reply(f"Your Whatsapp Number is not found !\nUse /verify to verify your whatsapp number \n\nWe just Upload your files to our <a href='{WHATSAPP_GROUP_LINK}'>group</a>",quote=True,disable_web_page_preview=True,parse_mode=ParseMode.HTML)

    await wabot.send_document(chat_id=whatsapp_id,Tg_id=message.from_user.id,Tg_mID=dm.id,FilePath=file,caption=message.caption)
    
