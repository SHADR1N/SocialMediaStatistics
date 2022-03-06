from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import re
import time 
import peewee
from vk_api import vk_api
import peewee
from datetime import datetime
import threading
from telethon import TelegramClient, events, utils
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.sessions import StringSession
import configparser
import sys
from bs4 import BeautifulSoup as bs
import requests

db = peewee.SqliteDatabase('db.sqlite3')
class BaseModel(peewee.Model):
    class Meta:
        database = db


class vk_bot_allpublic(BaseModel):
    source_public = peewee.TextField()
    name_public = peewee.TextField()
    link_public = peewee.TextField()


    @classmethod
    def get_row(cls, link_public):
        return cls.get(link_public == link_public)

    @classmethod
    def row_exists(cls, link_public):
        query = cls().select().where(cls.link_public == link_public)
        return query.exists()

    @classmethod
    def creat_row(cls, link_public,  name_public, source_public):
        user, created = cls.get_or_create(link_public=link_public, name_public = name_public, source_public = source_public)


class vk_bot_allpublication(BaseModel):
    source_publication = peewee.TextField()
    name_publication = peewee.TextField()
    view_publication = peewee.TextField()
    like_publication = peewee.TextField()
    repost_publication = peewee.TextField()
    comment_publication = peewee.TextField()
    date_publication = peewee.TextField()
    link_publication = peewee.TextField()

    favorite_publication = peewee.TextField()
    send_publication = peewee.TextField()
    views_publication = peewee.TextField()


    @classmethod
    def get_row(cls, link_publication):
        return cls.get(link_publication == link_publication)

    @classmethod
    def row_exists(cls, link_publication):
        query = cls().select().where(cls.link_publication == link_publication)
        return query.exists()

    @classmethod
    def creat_row(cls, link_publication):
        user, created = cls.get_or_create(link_publication=link_publication)

class vk_bot_statusparsmode(BaseModel):
    VK_status = peewee.TextField()
    TELEGRAM_status = peewee.TextField()


db.create_tables([vk_bot_statusparsmode])
db.create_tables([vk_bot_allpublication])
db.create_tables([vk_bot_allpublic])




value_posts = 100
val_group = 280

config = configparser.ConfigParser()
config.read(f"Settings.ini")
api_id = config['Settings']['api_id']
api_hash = config['Settings']['api_hash']
username = config['Settings']['username']
number_phone = config['Settings']['number_phone']
client = TelegramClient(username, api_id, api_hash)
client.start()



channel = sys.argv[1]
    
async def main(channel):
    offset = 0
    async for messages in client.iter_messages(channel):
        date = messages.date
        date = date.strftime('%Y-%m-%d')
        views = messages.views
        _id_ = messages.id
        link = 'https://t.me/'+str(channel)+'/'+str(_id_)
        if messages.replies != None:
            replies = messages.replies.replies
        else:
            replies = 0

        sender = await messages.get_sender() # получаем имя юзера
        name = utils.get_display_name(sender) # Имя Юзера
        chat_from = messages.chat if messages.chat else (await messages.get_chat()) # получаем имя группы
        chat_title = utils.get_display_name(chat_from)  # получаем имя группы


        if not vk_bot_allpublic.row_exists('https://t.me/'+str(channel)):
            name = chat_title
            source = 'Telegram'
            vk_bot_allpublic.creat_row('https://t.me/'+str(channel), name, source)
            print(chat_title)


        if views != None:
            if not vk_bot_allpublication.row_exists(link):
                ss = vk_bot_allpublication(source_publication = 'Telegram', 
                  name_publication = chat_title, 
                  view_publication = views, 
                  like_publication = 0, 
                  repost_publication = 0, 
                  comment_publication = replies, 
                  date_publication = date,
                  link_publication = link,
                  favorite_publication = 'Нет',
                  views_publication = 'Нет',
                  send_publication = 'Нет')
                ss.save()

            if vk_bot_allpublication.row_exists(link):
                old = vk_bot_allpublication.get(vk_bot_allpublication.link_publication == link )
                old.name_publication = chat_title
                old.view_publication = views
                old.like_publication = 0
                old.repost_publication = 0
                old.comment_publication = replies
                old.date_publication = date
                old.save()

            offset += 1
            if offset >= value_posts:
                break




with client:
    client.loop.run_until_complete(main(channel))
