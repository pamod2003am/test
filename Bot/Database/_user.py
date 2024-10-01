from pymongo import MongoClient
from ..Config import DATABASE_URL
from pyrogram.types import Message

user_db = None
db_connected = None
class UserDB:
    def users_db(self):
        global db_connected
        global user_db
        if db_connected:return user_db
        db = MongoClient(DATABASE_URL)['cluster2']
        db_connected = True
        user_db = db["users"]
        return user_db

    def __init__(self):
        self.user_db = self.users_db()

    def is_served_user(self,user_id: int) -> bool:
        user = self.user_db.find_one({"_id": user_id})
        if not user:
            return False
        return True

    def count_users(self) -> int:
        return self.user_db.count_documents({})

    def get_served_users(self) -> list:
        users = self.user_db.find({"_id": {"$gt": 0}})
        if not users:
            return []
        users_list = []
        for user in users:
            user = user.get("_id")
            users_list.append(user)
        return users_list

    def add_served_user(self,user_id: int):
        is_served = self.is_served_user(user_id)
        if is_served:
            return
        return  self.user_db.insert_one({"_id": user_id})
    
    def add_whatsapp_id(self,user_id: int, whatsapp_id: int):
        is_served = self.is_served_user(user_id)
        if not is_served:
            self.add_served_user(user_id)
        return  self.user_db.update_one({"_id": user_id}, {"$set": {"whatsapp_id": whatsapp_id}})
    
    def get_whatsapp_id(self,user_id: int):
        seved = self.user_db.find_one({"_id": user_id})
        if not seved:
            return
        return seved.get('whatsapp_id',None)
    
    def remove_served_user(self,user_id: int):
        is_served = self.is_served_user(user_id)
        if is_served:
            return
        return  self.user_db.delete_one({"_id": user_id})
    
def userDB(func):
    async def wrapper(bot, message: Message):
        user_id = message.from_user.id
        UserDB().add_served_user(user_id)
        await func(bot,message)
    return wrapper