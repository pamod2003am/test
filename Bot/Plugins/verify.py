from pyrogram import Client, filters 
from pyrogram.types import Message , ForceReply , InlineKeyboardButton , InlineKeyboardMarkup
import base64
from ..WaClient import StartWaClient
from ..Database import UserDB

def encrypt_phone_number(phone_number: str):
    return base64.b64encode(phone_number.encode('utf-8')).decode('utf-8')

def decrypt_phone_number(encrypted_phone: str):
    return base64.b64decode(encrypted_phone).decode('utf-8')

@Client.on_message(filters.command("verify"))
async def verify_command(client: Client, message: Message):
    await message.reply('Send me your Whatsapp Number',reply_markup=ForceReply(selective=True,placeholder='Ex: +9470xxxxxxx'),quote=True)    


@Client.on_message(filters.reply & filters.regex(r"^\+"))
async def verify_reply(client: Client, message: Message):
    if message.reply_to_message and message.reply_to_message.from_user.is_bot:
        if 'Send me your Whatsapp Number' in message.reply_to_message.text:
            await message.reply_to_message.delete()
            await message.delete()
            phone_number = message.text.replace('+','')
            _bot = (await client.get_me()).username
            whatsapp_id = f"{phone_number}@s.whatsapp.net"
            link = f"https://t.me/{_bot}/?start=VERIFY_{encrypt_phone_number(str(phone_number))}"
            wabot = await StartWaClient()
            myWA = str(wabot.me).replace('@s.whatsapp.net','')
            if ':' in myWA:myWA = myWA.split(':')[0]
            waLink = f"https://wa.me/{myWA}"
            keyboard = [[InlineKeyboardButton(url=waLink,text='Open Whatsapp')]]
            await wabot.send_message(chat_id=whatsapp_id,text=link)
            await message.reply(f'Confirm that the link has been sent to your whatsapp +{phone_number}',reply_markup=InlineKeyboardMarkup(keyboard))
            

async def verify_whatsapp(client: Client,message: Message,number):
    whatsapp_number = decrypt_phone_number(number)
    whatsapp_id = f"{whatsapp_number}@s.whatsapp.net"
    UserDB().add_whatsapp_id(user_id=message.from_user.id,whatsapp_id=whatsapp_id)
    await message.reply(f"+{whatsapp_number} successfully verified !")
