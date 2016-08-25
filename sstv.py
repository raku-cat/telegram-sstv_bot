import sys
import time
import telepot
import urllib.request
import glob,os
import subprocess
from PIL import Image
from random import randint
import pysox

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'photo':
        bot.sendMessage(chat_id, 'Downloading...')
        file_id = msg['photo'][-1]['file_id']
        pic = bot.getFile(file_id)
        file_path = pic['file_path']
        file_url = 'https://api.telegram.org/file/bot' + TOKEN + '/' + file_path
        urllib.request.urlretrieve(file_url, file_id + '.jpg')
        img = Image.open(file_id + '.jpg')
        size = 320, 256
        rondo = randint(0, 100)
        img.thumbnail(size, Image.ANTIALIAS)
        img.save(file_id + '.jpg', 'JPEG')
        bot.sendMessage(chat_id, 'Generating encoding...')
        subprocess.call(['pisstvpp', '-pm2', file_id + '.jpg'])
        bot.sendMessage(chat_id, 'Distorting encoding...')
        app = pysox.CSoxApp(file_id + '.jpg.wav', file_id + '.wav', effectparams=[ ("overdrive", [bytes(str(randint(60,100)), 'utf-8'), bytes(str(randint(1,40)), 'utf-8')] ), ("ladspa", [b'/usr/lib/ladspa/satan_maximiser_1408.so', bytes(str(randint(-90,-10)), 'utf-8'), bytes(str(randint(-100,-10)), 'utf-8')] ), ("ladspa", [b'/usr/lib/ladspa/valve_rect_1405.so', bytes(str(randint(1,100)), 'utf-8'), bytes(str(randint(1,100)), 'utf-8')] ), ("ladspa", [b'/usr/lib/ladspa/retro_flange_1208.so', bytes(str(randint(1,50)), 'utf-8'), bytes(str(randint(-500,90)), 'utf-8')] ),])
        app.flow()
        bot.sendMessage(chat_id, 'Sending...')
        bot.sendChatAction(chat_id, 'upload_audio')
        bot.sendAudio(chat_id, open(file_id + '.wav', 'rb'), title=file_id, duration=61)
        for file in glob.glob(file_id + '*'):
           os.remove(file)
    else:
        bot.sendMessage(chat_id, 'Please send a compressed image (not through the file selector)')

TOKEN = open('token.txt', 'r').read()
bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Starting...')
while 1:
    time.sleep(10)
