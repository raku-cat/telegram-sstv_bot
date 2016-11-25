#!/usr/bin/env python3
import sys
import time
import telepot
import requests
import glob,os
import subprocess
from PIL import Image
from random import randint
import pysox
from datetime import datetime
from pysstv.color import MartinM2

with open('token.txt', 'r') as f:
	token=f.read().strip('\n')
bot = telepot.Bot(token)
directory = '/tmp/sstvbot/'
if not os.path.exists(directory):
	os.makedirs(directory)

def handle(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	print(content_type, chat_type, chat_id)
	if content_type == 'photo':
		print('Recieved message from ' + str(chat_id))
		for file in glob.glob(directory + '*'):
			os.remove(file)
		curtime = datetime.now().strftime("%Y%m%d-%H%M%f")
		initial = bot.sendMessage(chat_id, 'Downloading...')
		msg_ider = telepot.message_identifier(initial)
		file_id = msg['photo'][-1]['file_id']
		pic = bot.getFile(file_id)
		file_url = 'https://api.telegram.org/file/bot' + token + '/' + bot.getFile(file_id)['file_path']
		img_file = directory + file_id + '.jpg'
		r = requests.get(file_url)
		if r.status_code == 200:
			with open(img_file, 'wb') as f:
				for chunk in r:
					f.write(chunk)
		img = Image.open(directory + file_id + '.jpg')
		size = 320,256
		img.thumbnail(size, Image.ANTIALIAS)
		background = Image.new('RGBA', size, (0, 0, 0, 0))
		background.paste(
			img,
			((size[0] - img.size[0]) // 2, (size[1] - img.size[1]) // 2))
		background.save(img_file, 'JPEG')
		bot.editMessageText(msg_ider, 'Generating encoding...')
		print('Generating encoding...', end="")
		MartinM2(Image.open(img_file), 28000, 16).write_wav(directory + file_id + '.jpg.wav')
		print('Done')
		bot.editMessageText(msg_ider, 'Distorting encoding...')
		print('Distorting...', end="")
		pysox.CSoxApp(directory + file_id + '.jpg.wav', directory + curtime + '.wav', effectparams=[ ("overdrive", [bytes(str(randint(60,100)), 'utf-8'), bytes(str(randint(1,40)), 'utf-8')] ), ("ladspa", [b'/usr/lib/ladspa/satan_maximiser_1408.so', bytes(str(randint(-90,-10)), 'utf-8'), bytes(str(randint(-100,-10)), 'utf-8')] ), ("ladspa", [b'/usr/lib/ladspa/valve_rect_1405.so', bytes(str(randint(1,100)), 'utf-8'), bytes(str(randint(1,100)), 'utf-8')] ), ("ladspa", [b'/usr/lib/ladspa/retro_flange_1208.so', bytes(str(randint(1,50)), 'utf-8'), bytes(str(randint(-500,90)), 'utf-8')] ),]).flow()
		print('Done')
		print('Sending')
		bot.editMessageText(msg_ider, 'Sending...')
		bot.sendChatAction(chat_id, 'upload_audio')
		bot.sendAudio(chat_id, open(directory + curtime + '.wav', 'rb'), title=curtime, duration=58)
	else:
		bot.sendMessage(chat_id, 'Please send a compressed image (not through the file selector)')

bot.message_loop(handle, run_forever='Started...')
