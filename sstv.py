#!/usr/bin/env python3
import sys
import time
import telepot
import urllib.request
import glob,os
import subprocess
from PIL import Image
from random import randint
import pysox
from datetime import datetime

TOKEN = open('token.txt', 'r').read()
bot = telepot.Bot(TOKEN)
directory = '/tmp/sstvbot/'
if not os.path.exists(directory):
	os.makedirs(directory)
print ('Started...')

def handle(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	print(content_type, chat_type, chat_id)
	if content_type == 'photo':
		curtime = datetime.now().strftime("%Y%m%e-%H%M%f")
		initial = bot.sendMessage(chat_id, 'Downloading...')
		msg_ider = telepot.message_identifier(initial)
		file_id = msg['photo'][-1]['file_id']
		pic = bot.getFile(file_id)
		file_url = 'https://api.telegram.org/file/bot' + TOKEN + '/' + bot.getFile(file_id)['file_path']
		urllib.request.urlretrieve(file_url, directory + file_id + '.jpg')
		img = Image.open(directory + file_id + '.jpg')
		img.thumbnail([320, 256], Image.ANTIALIAS)
		img.save(directory + file_id + '.jpg', 'JPEG')
		bot.editMessageText(msg_ider, 'Generating encoding...')
		print('Generating encoding...', end="")
		subprocess.call(['pisstvpp', '-pm2', directory + file_id + '.jpg'], stdout=open(os.devnull, 'wb'))
		print('Done')
		bot.editMessageText(msg_ider, 'Distorting encoding...')
		print('Distorting...', end="")
		pysox.CSoxApp(directory + file_id + '.jpg.wav', directory + curtime + '.wav', effectparams=[ ("overdrive", [bytes(str(randint(60,100)), 'utf-8'), bytes(str(randint(1,40)), 'utf-8')] ), ("ladspa", [b'/usr/lib/ladspa/satan_maximiser_1408.so', bytes(str(randint(-90,-10)), 'utf-8'), bytes(str(randint(-100,-10)), 'utf-8')] ), ("ladspa", [b'/usr/lib/ladspa/valve_rect_1405.so', bytes(str(randint(1,100)), 'utf-8'), bytes(str(randint(1,100)), 'utf-8')] ), ("ladspa", [b'/usr/lib/ladspa/retro_flange_1208.so', bytes(str(randint(1,50)), 'utf-8'), bytes(str(randint(-500,90)), 'utf-8')] ),]).flow()
		print('Done')
		print('Sending')
		bot.editMessageText(msg_ider, 'Sending...')
		bot.sendChatAction(chat_id, 'upload_audio')
		bot.sendAudio(chat_id, open(directory + curtime + '.wav', 'rb'), title=curtime, duration=61)
		for file in glob.glob(directory + '*'):
			os.remove(file)
	else:
		bot.sendMessage(chat_id, 'Please send a compressed image (not through the file selector)')

bot.message_loop(handle)
while 1:
	time.sleep(10)
