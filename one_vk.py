
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
from telethon import TelegramClient, events
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

app_id = 6818340
token = '8f87fbf68f87fbf68f87fbf6668feff1d288f878f87fbf6d3bc41660e11a9b829564185'



link =  sys.argv[1]

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0(X11;Linux x86_64...)Geco/20100101 Firefox/60.0'}

session = requests.session()
request = session.get(link, headers=headers)
if request.status_code == 200:
    soup = bs(request.content, 'html.parser')
    owner_id = '-'+str(soup).split('(event, -')[1].split(',')[0] 
    name_public = soup.find('title').text
    name_public = name_public.replace('| ВКонтакте', '')


vk_session = vk_api.VkApi(app_id=app_id, token=token)
vk = vk_session.get_api()

offset = 0
count = 100

if not vk_bot_allpublic.row_exists(owner_id[1:]):
    vk_bot_allpublic.creat_row(owner_id[1:], name_public, 'VK')


while True:
    try:
        posts = vk.wall.get(owner_id = owner_id, offset=offset, count=count)
        views = posts['items']
        all_post = posts['count']

        for el in views:
        
            com = el['comments']['count']
            lik = el['likes']['count']
            viw = el['views']['count']
            id_ = el['id']
            date = el['date']
            date = (datetime.fromtimestamp(date).strftime('%Y-%m-%d'))
            rep = el['reposts']['count']
            link = f'https://vk.com/wall{owner_id}?own=1&w=wall{owner_id}_{id_}'
            #print(viw)
            if not vk_bot_allpublication.row_exists(link):
                ss = vk_bot_allpublication(source_publication = 'VK', 
                  name_publication = name_public, 
                  view_publication = viw, 
                  like_publication = lik, 
                  repost_publication = rep, 
                  comment_publication = com, 
                  date_publication = date,
                  link_publication = link,                               
                  favorite_publication = 'Нет',
                  views_publication = 'Нет',
                  send_publication = 'Нет')
                ss.save()

            if vk_bot_allpublication.row_exists(link):
                old = vk_bot_allpublication.get(vk_bot_allpublication.link_publication == link )
                old.name_publication = name_public
                old.view_publication = viw
                old.like_publication = lik
                old.repost_publication = rep
                old.comment_publication = com
                old.date_publication = date
                old.save()
        
        if count >= value_posts:
            break

        
        offset += 1
        count += 100

    except:
        pass