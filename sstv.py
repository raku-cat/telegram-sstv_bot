import sys
import time
import telepot
import urllib.request
import glob,os
import subprocess
from PIL import Image
from random import randint
import pysox
import time

TOKEN = open('token.txt', 'r').read()
bot = telepot.Bot(TOKEN)
print ('Started...')

def handle(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	print(content_type, chat_type, chat_id)
	if content_type == 'photo':
		curtime = time.strftime("%Y%m%e-%H%M")
		initial = bot.sendMessage(chat_id, 'Downloading...')
		msg_ider = telepot.message_identifier(initial)
		file_id = msg['photo'][-1]['file_id']
		pic = bot.getFile(file_id)
		file_path = pic['file_path']
		file_url = 'https://api.telegram.org/file/bot' + TOKEN + '/' + file_path
		urllib.request.urlretrieve(file_url, file_id + '.jpg')
		img = Image.open(file_id + '.jpg')
		size = 320, 256
		img.thumbnail(size, Image.ANTIALIAS)
		img.save(file_id + '.jpg', 'JPEG')
		bot.editMessageText(msg_ider, 'Generating encoding...')
		subprocess.call(['pisstvpp', '-pm2', file_id + '.jpg'])
		bot.editMessageText(msg_ider, 'Distorting encoding...')
		app = pysox.CSoxApp(file_id + '.jpg.wav', curtime + '.wav', effectparams=[ ("overdrive", [bytes(str(randint(60,100)), 'utf-8'), bytes(str(randint(1,40)), 'utf-8')] ), ("ladspa", [b'/usr/lib/ladspa/satan_maximiser_1408.so', bytes(str(randint(-90,-10)), 'utf-8'), bytes(str(randint(-100,-10)), 'utf-8')] ), ("ladspa", [b'/usr/lib/ladspa/valve_rect_1405.so', bytes(str(randint(1,100)), 'utf-8'), bytes(str(randint(1,100)), 'utf-8')] ), ("ladspa", [b'/usr/lib/ladspa/retro_flange_1208.so', bytes(str(randint(1,50)), 'utf-8'), bytes(str(randint(-500,90)), 'utf-8')] ),])
		app.flow()
		bot.editMessageText(msg_ider, 'Sending...')
		bot.sendChatAction(chat_id, 'upload_audio')
		bot.sendAudio(chat_id, open(curtime + '.wav', 'rb'), title=curtime, duration=61)
		for file in glob.glob(file_id + '*', curtime + '.wav'):
			os.remove(file)
	else:
		bot.sendMessage(chat_id, 'Please send a compressed image (not through the file selector)')

bot.message_loop(handle)
while 1:
	time.sleep(10)
