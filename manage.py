#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys, subprocess
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import re
import time 
import peewee
#from vk_group




db = peewee.SqliteDatabase('db.sqlite3')
class BaseModel(peewee.Model):
    class Meta:
        database = db


class vk_bot_statusparsmode(BaseModel):
    VK_status = peewee.TextField()
    TELEGRAM_status = peewee.TextField()

db.create_tables([vk_bot_statusparsmode])

def main():

    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SOCIALBOT.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)




if __name__ == '__main__': 
    #threading.Thread(target=WhileStart).start()  
    main()

