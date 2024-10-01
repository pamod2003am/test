from pyrogram import Client
import subprocess
import threading
import asyncio
import qrcode
import shutil
import os
import sys

from .Auth import send_qr_func

def get_mime(ext): 
    MIME_TYPE = {
        'txt': 'text/plain',
        'csv': 'text/csv',
        'log': 'text/plain',
        'md': 'text/markdown',
        'py': 'text/x-python',
        'html': 'text/html',
        'css': 'text/css',
        'js': 'application/javascript',
        'json': 'application/json',
        'xml': 'application/xml',
        'java': 'text/x-java-source',
        'php': 'application/x-httpd-php',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'bmp': 'image/bmp',
        'svg': 'image/svg+xml',
        'tiff': 'image/tiff',
        'ico': 'image/x-icon',
        'mp3': 'audio/mpeg',
        'wav': 'audio/wav',
        'ogg': 'audio/ogg',
        'flac': 'audio/flac',
        'aac': 'audio/aac',
        'mp4': 'video/mp4',
        'mkv': 'video/x-matroska',
        'webm': 'video/webm',
        'avi': 'video/x-msvideo',
        'mov': 'video/quicktime',
        'wmv': 'video/x-ms-wmv',
        'pdf': 'application/pdf',
        'doc': 'application/msword',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'xls': 'application/vnd.ms-excel',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'ppt': 'application/vnd.ms-powerpoint',
        'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'zip': 'application/zip',
        'rar': 'application/x-rar-compressed',
        '7z': 'application/x-7z-compressed',
        'tar': 'application/x-tar',
        'gz': 'application/gzip',
        'exe': 'application/octet-stream',
        'iso': 'application/x-iso9660-image',
        'apk': 'application/vnd.android.package-archive',
        'ttf': 'font/ttf',
        'woff': 'font/woff',
        'woff2': 'font/woff2',
        'csv': 'text/csv',
        'ics': 'text/calendar',
        'epub': 'application/epub+zip',
        'mp3': 'audio/mpeg',
        'wav': 'audio/wav',
        'ogg': 'audio/ogg',
        'm4a': 'audio/mp4',
        'aac': 'audio/aac',
        'flac': 'audio/flac',
        'weba': 'audio/webm',
        'amr': 'audio/amr',
        'opus': 'audio/opus',
      }

    return MIME_TYPE.get(ext, 'application/octet-stream')

def generate_qr(data, filename='qr.png'):
    qr = qrcode.QRCode(
        version=1, 
        error_correction=qrcode.constants.ERROR_CORRECT_L, 
        box_size=8,  
        border=1,)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)
    return filename

class WAClient:
    def __init__(self,bot):
        self.__process = None
        self.__loop = asyncio.get_event_loop()
        self.tgBot : Client = bot
        
    def __read_output(self):
        while True:
            output = self.__process.stdout.readline()
            if output:
                out = output.strip()
                if out.startswith("TG_TIGGER"):
                    data = out.replace("TG_TIGGER:","")
                    asyncio.run_coroutine_threadsafe(self.__trigger_async_function(data), self.__loop)
                # else:
                #     print(out)
            if self.__process.poll() is not None:  
                error = self.__process.stderr.readline()
                if error:
                    print(f'Error from Node.js: {error.strip()}')
                    self.restart_node_process()

    async def polling(self):
        print("WaClient Started")
        for item in os.listdir("Bot/downloads"):
            item_path = os.path.join("Bot/downloads", item)
            shutil.rmtree(item_path) if os.path.isdir(item_path) else os.remove(item_path)
        self.__process = subprocess.Popen(
            args=['node','Bot/WaClient/client.js'], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            stdin=subprocess.PIPE,
            text=True
            )
        await asyncio.sleep(5)
        self.__read_thread = threading.Thread(target=self.__read_output)
        self.__read_thread.start()
    
    def restart_node_process(self):
        if self.__process:
            self.__process.terminate() 
            self.__process.wait()  
        asyncio.run(self.polling())

    async def __do_post__(self,command,data):
        command = f"{command}|{data}"
        if self.__process.stdin:
            self.__process.stdin.write(command)  
            self.__process.stdin.flush()
        await asyncio.sleep(1)

    async def __trigger_async_function(self, data: str):
        if data.startswith('QR'):
            qr_data= data.replace('QR:','')
            img = generate_qr(qr_data)
            await send_qr_func(self.tgBot,img)
        if data.startswith('ME'):
            self.me = data.replace('ME:','')
        if data.startswith('Connected'):
            await send_qr_func(self.tgBot,'test',connected=True)
            print("Connected")

        if data.startswith('doc'):
                user_id,message_id,ufile ,_ = data.replace('doc:','').split(':')
                await self.tgBot.edit_message_text(chat_id=int(user_id),message_id=int(message_id),text='Upload Complete')
                await asyncio.sleep(2)
                await self.tgBot.delete_messages(chat_id=user_id,message_ids=[int(message_id)])
                if os.path.exists(ufile.strip()):
                    os.remove(ufile.strip())
           
        if data.startswith('Logged'):
            print("logout")

    async def send_message(self,chat_id: str,text: str):
        command = "sendMessage"
        data = f"{chat_id},{text}"
        await self.__do_post__(command,data)

    async def send_image(self,chat_id,Image_url,caption):
        command = "sendImage"
        data = f"{chat_id},{Image_url},{caption}"
        await self.__do_post__(command,data)

    async def send_document(self,chat_id: str,Tg_id: int,Tg_mID: int,FilePath: str,caption: str):
        command = "sendDocument"
        fileName = str(FilePath).split('/')[-1] if '/' in str(FilePath) else FilePath
        extention = fileName.split(".")[-1]
        mimeType = get_mime(extention)
        data = f"{chat_id},{Tg_id},{Tg_mID},{FilePath},{fileName},{mimeType},{caption}"
        await self.__do_post__(command,data)


    async def send_video(self,chat_id,video,caption):
        command = "sendVideo"
        data = f"{chat_id},{video},{caption}"
        await self.__do_post__(command,data)

    async def send_audio(self,chat_id: str,audio: str,send_as_voice: bool = False):
        command = "sendVoice" if send_as_voice else "sendAudio"
        extention = audio.split('.')[-1]
        mimeType = get_mime(extention)
        data = f"{chat_id},{audio},{mimeType}"
        print(data)
        await self.__do_post__(command,data)

    async def send_sticker(self,chat_id: str,sticker: str):
        command = "sendSticker"
        data = f"{chat_id},{sticker}"
        await self.__do_post__(command,data)
