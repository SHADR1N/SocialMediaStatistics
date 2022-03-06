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
import os

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
    def creat_row(cls, link_public):
        user, created = cls.get_or_create(link_public=link_public)


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
val_group = 5000

def Get_link_vk():
    offset = 0
    try:
        chrome_options = Options()  
        chrome_options.add_argument(f"--user-data-dir={os.getcwd()}/VKProfile")
        chrome_options.add_argument(f"--headless")
        driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=chrome_options)
    except:
        driver.close()
        return

    for el in range(int(val_group/50)):

        link = f'https://allsocial.ru/communities/?offset={offset}'
        driver.get(link)
        time.sleep(10)

        list_ = driver.find_element_by_xpath('//ul[@class="list ng-scope"]')

        for ele in list_.find_elements_by_xpath('.//li[@class="item ng-scope"]')[1:]:
            name = (  ele.find_element_by_xpath('.//span[@class="caption"]').text  )
            subs = ( ele.find_element_by_xpath('.//div[@class="quantity"]').text )
            a = ( ele.find_element_by_xpath('.//a[@bo-href="item.href"]').get_attribute('href') )

            if 'public' in a:
                a = a.split('public')[1]
                #print(a)

            if 'club' in a:
                a = a.split('club')[1]
                #print(a)

            links = a
            print(name)
            if not vk_bot_allpublic.row_exists(links):
                ss = vk_bot_allpublic(source_public = 'VK', name_public = name, link_public = links)
                ss.save()
        offset += 25
    driver.quit()
    Get_publication_vk()

def Get_publication_vk():
    for el in vk_bot_allpublic.select():
        if el.source_public == 'VK':
            app_id = 0
            token = ''

            owner_id = int(str('-')+str(el.link_public))
            name_public = el.name_public
            vk_session = vk_api.VkApi(app_id=app_id, token=token)
            vk = vk_session.get_api()

            offset = 0
            count = 100

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

def Get_link_telegram():

    pk = val_group
    for pk in range(int(pk/30)):
        try:
            link = f'https://telemetr.me/channels/?page={pk}'

            headers = {'accept': '*/*',
                       'user-agent': 'Mozilla/5.0(X11;Linux x86_64...)Geco/20100101 Firefox/60.0'}

            session = requests.session()
            request = session.get(link, headers=headers)
            if request.status_code == 200:
                soup = bs(request.content, 'html.parser')

                attr = soup.find('table', attrs = {'id': "channels_table"}).find('tbody')
                tr = attr.findAll('tr', class_= "tr_even")

                for el in attr.findAll('tr', class_= "tr_even"):
                    if len(el) > 10:
                        href = el.find('a', attrs = {'target': '_blank'}).get('href')
                        name = el.find('td', class_="wd-300 pb-0").find('a', attrs = {'target': '_blank'}).text
                        links = 'https://t.me/'+str(href.split('/')[-1])

                        if not vk_bot_allpublic.row_exists(links):
                            ss = vk_bot_allpublic(source_public = 'Telegram', name_public = name, link_public = links)
                            ss.save()
                            print(links, name)

        except:
            time.sleep(10)
            pk -= 1

    Get_publication_telegram()

def Get_publication_telegram():

    for el in vk_bot_allpublic.select():
        try:
            if el.source_public == 'Telegram':
                name_public = el.name_public
                channel = el.link_public
                channel = channel.split('t.me/')[1].strip()

                config = configparser.ConfigParser()
                config.read(f"Settings.ini")
                api_id = config['Settings']['api_id']
                api_hash = config['Settings']['api_hash']
                username = config['Settings']['username']
                number_phone = config['Settings']['number_phone']
                client = TelegramClient(username, api_id, api_hash)
                client.start()


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

                        #print(date, views, replies, link)
                        if views != None:
                            #print(date)
                            if not vk_bot_allpublication.row_exists(link):
                                ss = vk_bot_allpublication(source_publication = 'Telegram', 
                                  name_publication = name_public, 
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
                                old.name_publication = name_public
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


        except ValueError:
            print('Канал не найден:', channel)
            pass

    time.sleep(50)      

def WhileStart():
    x = 0
    while True:
        if x == 0:
            t = threading.Thread(target=Get_link_vk)
            t.start()

            w = threading.Thread(target=Get_link_telegram)
            w.start()
            x += 1
            time.sleep(86400)
            x = 0

WhileStart()