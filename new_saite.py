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


pk = 10

for pk in range(pk):
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
			    	href = 'https://t.me/'+str(href.split('/')[-1])
			    	
			    	print(href, name)

	except:
		pass