import os
import sys, subprocess
import threading





def start_1():
	os.system('python vk_group.py')


def start_2():
	os.system('python manage.py runserver')

	
threading.Thread(target = start_1).start()
threading.Thread(target = start_2).start()