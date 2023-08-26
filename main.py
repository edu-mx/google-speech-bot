# diaseduardo139@gmail.com
import os
import logging as log
from random import randint as rand
import telebot
from gtts import gTTS
log.basicConfig(level=log.ERROR, filename='bot_log.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

# token in token_bot.txt
def get_token_bot(filename='token_bot.txt'):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            token = file.read().strip()
            return token
    except FileNotFoundError as x:
        log.error('Token not found %s' % (x))
        exit('The token_bot.txt file does not exist, create it and add the bot token there;')
        return
    finally:
        file.close()

def TTS(text_voice='Hello: 1, 2, 3.', lang_voice='en'):
    try:
        tts_voice = gTTS(text_voice, lang=lang_voice)
        folder = 'files'
        audioTempFile = f'{folder}/Audio_{rand(100, 999)}_{lang_voice}.mp3'
        if not os.path.exists(folder):
            os.makedirs(folder)
        tts_voice.save(audioTempFile)
        return audioTempFile
    except Exception as x:
        log.critical('Não foi possível salvar o arquivo %s' % (x))
        return

token_bot = get_token_bot()
if token_bot:
    bot = telebot.TeleBot(token_bot)
else: exit('The file does not have a token, please open token_bot.txt and check its integrity.')
