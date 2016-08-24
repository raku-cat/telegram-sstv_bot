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
#    file_id = msg['photo'][-1]['file_id']
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'photo':
        file_id = msg['photo'][-1]['file_id']
        picz = bot.getFile(file_id)
        thisisit = picz['file_path']
#        print(picz)
#        print(thisisit)
#        print('https://api.telegram.org/file/bot' + TOKEN + '/' + thisisit)
        theone = 'https://api.telegram.org/file/bot' + TOKEN + '/' + thisisit
        urllib.request.urlretrieve(theone, file_id + '.jpg')
        img = Image.open(file_id + '.jpg')
        size = 320, 256
        rondo = randint(0, 100)
        img.thumbnail(size, Image.ANTIALIAS)
        img.save(file_id + '.jpg', 'JPEG')
        subprocess.call(['pisstvpp', '-pm2', file_id + '.jpg'])
   #     subprocess.call(['sox', file_id + '.jpg.wav', file_id + '.wav', 'overdrive', str(randint(1,100)), str(randint(1,100)), 'bend'] + [str(randint(1,10)),str(randint(1,800)),str(randint(1,8))])
        distrt = ','.join(map(str, [randint(1,4), randint(1,300), randint(1,8)]))
        finald = bytes(distrt, 'utf-8')
        app = pysox.CSoxApp(file_id + '.jpg.wav', file_id + '.wav', effectparams=[ ("overdrive", [bytes(str(randint(1,100)), 'utf-8'), bytes(str(randint(1,100)), 'utf-8')] ), ("bend", [finald]), ])
        app.flow()
        bot.sendChatAction(chat_id, 'upload_audio')
        bot.sendAudio(chat_id, open(file_id + '.wav', 'rb'), title=file_id, duration=61)
#        subprocess.call(['rm', file_id + '.jpg', file_id + '.jpg.wav', file_id + '.wav'])
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
