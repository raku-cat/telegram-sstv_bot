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
from pysstv.color import MartinM2

TOKEN = open('token.txt', 'r').read()
bot = telepot.Bot(TOKEN)
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
		urllib.request.urlretrieve(file_url, file_id + '.jpg')
		img = Image.open(file_id + '.jpg')
		img.thumbnail([320, 256], Image.ANTIALIAS)
		img.save(file_id + '.jpg', 'JPEG')
		bot.editMessageText(msg_ider, 'Generating encoding...')
		MartinM2(img, 28000, 16).write_wav(file_id + '.jpg.wav')
		bot.editMessageText(msg_ider, 'Distorting encoding...')
		pysox.CSoxApp(file_id + '.jpg.wav', curtime + '.wav', effectparams=[ ("overdrive", [bytes(str(randint(60,100)), 'utf-8'), bytes(str(randint(1,40)), 'utf-8')] ), ("ladspa", [b'/usr/lib/ladspa/satan_maximiser_1408.so', bytes(str(randint(-90,-10)), 'utf-8'), bytes(str(randint(-100,-10)), 'utf-8')] ), ("ladspa", [b'/usr/lib/ladspa/valve_rect_1405.so', bytes(str(randint(1,100)), 'utf-8'), bytes(str(randint(1,100)), 'utf-8')] ), ("ladspa", [b'/usr/lib/ladspa/retro_flange_1208.so', bytes(str(randint(1,50)), 'utf-8'), bytes(str(randint(-500,90)), 'utf-8')] ),]).flow()
		bot.editMessageText(msg_ider, 'Sending...')
		bot.sendChatAction(chat_id, 'upload_audio')
		bot.sendAudio(chat_id, open(curtime + '.wav', 'rb'), title=curtime, duration=61)
		for file in glob.glob(file_id + '*'):
			os.remove(file)
		os.remove(curtime + '.wav')
	else:
		bot.sendMessage(chat_id, 'Please send a compressed image (not through the file selector)')

bot.message_loop(handle)
while 1:
	time.sleep(10)
