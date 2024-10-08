const { DisconnectReason, useMultiFileAuthState ,Browsers} = require("@whiskeysockets/baileys");
const useMongoDBAuthState = require("./mongoAuthState");
const { readFileSync } = require('fs');
const makeWASocket = require("@whiskeysockets/baileys").default;
const pino = require('pino');

const mongoURL = "mongodb+srv://pamod:pamod123@cluster0.nwfe5np.mongodb.net";
const mongoDbUrl = 'mongodb+srv://pamod:pamod123@cluster0.nwfe5np.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
const { MongoClient } = require("mongodb");


class Client {
    constructor() {
        this.Bot = null;
    }
    async connect() {
        const mongoClient = new MongoClient(mongoDbUrl, {});
        await mongoClient.connect();
        const collection = mongoClient.db("whatsapp_api").collection("auth");
        const { state, saveCreds } = await useMongoDBAuthState(collection);
        this.Bot = makeWASocket({
            logger: pino({ level: 'silent' }) ,
            printQRInTerminal: true,
            auth: state,
        });
        console.log(`TG_TIGGER:ME:${this.Bot?.user?.id}`);
        this.Bot.ev.on('creds.update', saveCreds);
        this.Bot.ev.on('connection.update', async (update) => {
            const { connection, lastDisconnect, qr } = update || {};
            
            if (qr) { console.log(`TG_TIGGER:QR:${qr}`); }
            if (connection === 'open') {console.log('TG_TIGGER:Connected');}
            if (connection === 'close') {
                const disconnectReason = lastDisconnect?.error?.output?.statusCode;
                if (disconnectReason === DisconnectReason.loggedOut) {
                    console.log('TG_TIGGER:Logged out from WhatsApp');
                    await mongoClient.db('whatsapp_api').dropCollection('auth')
                    this.connect();
                }
                const shouldReconnect = lastDisconnect?.error?.output?.statusCode !== DisconnectReason.loggedOut;
                if (shouldReconnect) { this.connect(); }
            }
        });
        this.Bot.ev.on('messages.upsert', m => {
            var chat_id = m.messages[0].key.remoteJid
            console.log(chat_id)
            var text = m.messages[0].message.conversation
            if(text == 'Hi'){
                const react = {react: {text: "🔁",key: m.messages[0].key}}
                const Noreact = {react: {text: "",key: m.messages[0].key}}
                setTimeout(() => {this.Bot.sendMessage(chat_id,react)}, 500);
                setTimeout(() => {this.Bot.sendMessage(chat_id,{ text: 'Hello there!' }, { quoted: m.messages[0] })}, 1000);
                setTimeout(() => {this.Bot.sendMessage(chat_id,Noreact)}, 1500);
            }   
        })
    }

    async SendMessage(chatID, message) {
        if (!this.Bot) {await this.connect();}
        const msg = await this.Bot.sendMessage(chatID, { text: message });
        return msg.key.id; 
    }
    async SendImage(chatID, imageUrl,caption){
        if (!this.Bot) {await this.connect();}
        const msg = await this.Bot.sendMessage(chatID, {image: {url: imageUrl},caption: caption})
        return msg.key.id; 
    }
    async  SendDocument(chatID, filePath , fileName ,mimetype , caption) {
        if (!this.Bot) {
            await this.connect();}
        const buffer = readFileSync(filePath); 
        const msg = await this.Bot.sendMessage(chatID, {
            document: buffer, 
            mimetype: mimetype,
            fileName: fileName,
            caption: caption
        }
    );
        return msg.key.id
    }

    async SendVideo(chatID,video,caption,mimetype){
        if (!this.Bot) {
            await this.connect();
        }
        const msg = await this.Bot.sendMessage(chatID, {
            video: { url: video},
            caption: caption,
            mimetype: mimetype, 
        })
        return msg.key.id
    }

    async SendAudio(chatID,audio,mimetype){
        if (!this.Bot) {
            await this.connect();
        }
        const msg = await this.Bot.sendMessage(chatID, {
            audio: { url: audio},
            mimetype: mimetype, 
        })
        return msg.key.id
    }
    async SendVoice(chatID,audio,mimetype){
        if (!this.Bot) {
            await this.connect();
        }
        const msg = await this.Bot.sendMessage(chatID, {
            audio: { url: audio},
            mimetype: mimetype, 
            ptt: true 
        })
        return msg.key.id
    }
    

    async SendSticker(chatID,sticker){
        if (!this.Bot) {
            await this.connect();
        }
        const msg = await this.Bot.sendMessage(chatID, {
            sticker: { url: sticker}
        })
        return msg.key.id
    }
    async sendStatus(){
        sock.sendMessage(jid, {image: {url: url}, caption: caption}, {backgroundColor : backgroundColor, font : font, statusJidList: statusJidList, broadcast : true})
    }
}

// const http = require('http');
// const healthCheckPort = 8443; 
// const healthCheckServer = http.createServer((req, res) => {
//     if (req.method === 'GET' && req.url === '/health') {
//         res.writeHead(200, { 'Content-Type': 'text/plain' });
//         res.end('OK\n');
//     } else {
//         res.writeHead(404);
//         res.end();
//     }
// });

// healthCheckServer.listen(healthCheckPort, () => {
//     console.log(`Health check server running on port ${healthCheckPort}`);
// });




const botClient = new Client();

async function startListening() {
    await botClient.connect();
    console.log("WAClient Started")

    process.stdin.on('data', async (data) => {
        const input = data.toString().trim();
        const [ command, mdata ] = input.split('|'); 
        

        if (command === 'sendMessage') {
            const [chatId,message] = mdata.split(',');
            const msgId = await botClient.SendMessage(chatId, message);
            console.log(`Message ID : ${msgId}`); 
        }
        if (command === 'sendImage'){
            const [chatId,imageUrl,caption] = mdata.split(',');
            const msgId = await botClient.SendImage(chatId, imageUrl,caption);
            console.log(`Message ID : ${msgId}`); 
        }
        if(command === 'sendDocument'){
            const [chatId,Tg_ID,Tg_mID,filePath,fileName,mimetype,caption] = mdata.split(',');
            const msgId = await botClient.SendDocument(chatId,filePath,fileName,mimetype,caption)
            console.log(`TG_TIGGER:doc:${Tg_ID}:${Tg_mID}:${filePath}:${msgId}`); 
        }
        if(command === 'sendVideo'){
            const [chatId,video,caption,mimetype] = mdata.split(',');
            const msgId = await botClient.SendVideo(chatId,video,caption,mimetype)
            console.log(`Message ID : ${msgId}`);
        }
        if(command === 'sendAudio'){
            const [chatId,audio,mimetype] = mdata.split(',');
            const msgId = await botClient.SendAudio(chatId,audio,mimetype)
            console.log(`Message ID : ${msgId}`);
        }
        if (command === 'sendSticker'){
            const [chatId,sticker] = mdata.split(',');
            const msgId = await botClient.SendSticker(chatId,sticker)
            console.log(`Message ID : ${msgId}`);
        }
        if(command === 'sendVoice'){
            const [chatId,audio,mimetype] = mdata.split(',');
            const msgId = await botClient.SendVoice(chatId,audio,mimetype)
            console.log(`Message ID : ${msgId}`);
        }

        // sendContact
        // sendLocation
        // sendPoll
        
    });
}
startListening();
module.exports = { startListening };
