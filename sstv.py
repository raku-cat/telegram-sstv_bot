import sys
import time
import telepot
import urllib.request
import subprocess

def handle(msg):
    file_id = msg['photo'][-1]['file_id']
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id, file_id)

    if content_type == 'photo':
        picz = bot.getFile(file_id)
        thisisit = picz['file_path']
        print(picz)
        print(thisisit)
        print('https://api.telegram.org/file/bot' + TOKEN + '/' + thisisit)
        theone = 'https://api.telegram.org/file/bot' + TOKEN + '/' + thisisit
        urllib.request.urlretrieve(theone, file_id + '.jpg')
        subprocess.call(['pisstvpp', '-pm2', file_id + '.jpg'])
        bot.sendChatAction(chat_id, 'upload_audio')
        bot.sendAudio(chat_id, open(file_id + '.jpg.wav', 'rb'), title=file_id)
        subprocess.call(['rm', file_id + '.jpg'])
        subprocess.call(['rm', file_id + '.jpg.wav'])

TOKEN = open('token.txt', 'r').read()
bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Starting...')
while 1:
    time.sleep(10)
