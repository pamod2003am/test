from pyrogram import Client, filters 
from pyrogram.types import InputMediaPhoto
import os
import asyncio

QR_MSG_ID = None


def delete_image(image_path):
    if os.path.exists(image_path):
        os.remove(image_path)

async def connected_func(client:Client):
    global QR_MSG_ID
    if QR_MSG_ID:
        try:await client.delete_messages(chat_id=-1002126632607,message_ids=[QR_MSG_ID])
        except:pass
    m = await client.send_message(chat_id=-1002126632607,text='Connected !!')
    await asyncio.sleep(5)
    await m.delete()

async def show_qr(client:Client, qr_img:str):
    global QR_MSG_ID
    if QR_MSG_ID:
        try:
            media = InputMediaPhoto(media=qr_img, caption="Scan Qr code for loggin\n\nTimeout 40s",)
            await client.edit_message_media(chat_id=-1002126632607,message_id=QR_MSG_ID,media=media)
        except Exception as e:print(e)
    else:
        try:
            msg = await client.send_photo(chat_id=-1002126632607,photo=qr_img,caption='Scan Qr code for loggin\n\nTimeout 40s')
            QR_MSG_ID = msg.id
        except Exception as e:print(e)
    await asyncio.sleep(1)
    delete_image(qr_img)

async def send_qr_func(client:Client, qr_img:str,connected:bool = False):
    if connected:
        asyncio.create_task(connected_func(client))
    else:
        asyncio.create_task(show_qr(client,qr_img))
        


    
