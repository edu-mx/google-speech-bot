# diaseduardo139@gmail.com
import os
import logging as log
from random import randint as rand
from time import sleep
import telebot
from gtts import gTTS
log.basicConfig(level=log.ERROR, filename='bot_log.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

# language codes
langs = {
    'pt-br': 'Olá! Bem-vindo(a) a este bot. Eu posso transformar seus textos em áudio usando a API de Texto para Fala do Google (gTTS). Para começar, basta escolher o seu idioma preferido e começar a escrever seu texto. 🎉',
    'pt': 'Olá! Bem-vindo(a) a este bot. Eu posso transformar os seus textos em áudio usando a API de Texto para Fala do Google (gTTS). Para começar, escolha o seu idioma preferido e comece a escrever o seu texto. 🎉',
    'en': 'Hello! Welcome to this bot. I can transform your texts into audio using the Google Text-to-Speech API (gTTS). To get started, just select your preferred language and begin typing your text. 🎉',
    'es': '¡Hola! Bienvenido(a) a este bot. Puedo convertir tus textos en audio utilizando la API de Texto a Voz de Google (gTTS). Para comenzar, simplemente elige tu idioma preferido y comienza a escribir tu texto. 🎉',
    'tr': 'Merhaba! Bu bota hoş geldiniz. Google Metin-İşitme API (gTTS) kullanarak metinlerinizi ses dosyalarına dönüştürebilirim. Başlamak için sadece tercih ettiğiniz dili seçin ve metin yazmaya başlayın. 🎉',
    'fr': 'Bonjour ! Bienvenue sur ce bot. Je peux transformer vos textes en audio en utilisant l\'API Google Text-to-Speech (gTTS). Pour commencer, il vous suffit de choisir votre langue préférée et de commencer à taper votre texte. 🎉',
    'ru': 'Привет! Добро пожаловать в этого бота. Я могу преобразовать ваши тексты в аудио с помощью API Google Text-to-Speech (gTTS). Чтобы начать, просто выберите ваш предпочитаемый язык и начните вводить текст. 🎉',
    'de': 'Hallo! Willkommen bei diesem Bot. Ich kann Ihre Texte mithilfe der Google Text-to-Speech-API (gTTS) in Audio umwandeln. Um loszulegen, wählen Sie einfach Ihre bevorzugte Sprache aus und beginnen Sie mit dem Schreiben Ihres Textes. 🎉',
    'ja': 'こんにちは！このボットへようこそ。Googleテキスト読み上げAPI（gTTS）を使用してテキストを音声に変換できます。始めるには、好きな言語を選択してテキストを入力してください。 🎉',
    'zh': '你好！欢迎使用这个机器人。我可以使用Google的文本转语音API（gTTS）将您的文本转换为语音。要开始，请选择您喜欢的语言并开始输入文本。 🎉'
}

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

def send_audio(chat_id, filename, description):
    try:
    short_desc = f'{description[:30]}...'
    with open(filename, 'rb') as audio:
        bot.send_audio(chat_id, audio, caption=short_desc)
    except Exception as x:
        log.error('Unable to send audio %S. %S' %(filename, x))

import json
import os

def save_user(name, user_id, lang):
    filename = 'users_bot.json'
    data = {}

    # Verifica se o arquivo JSON existe antes de tentar carregá-lo
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
    else :
        with open('users.json', 'w', encoding='utf-8') as file:
    # Se o usuário ainda não existe no JSON, adiciona as informações
    if str(user_id) not in data:
        data[str(user_id)] = {'name': name, 'lang': lang}

        # Salva as informações atualizadas no arquivo JSON
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

token_bot = get_token_bot()
if token_bot:
    bot = telebot.TeleBot(token_bot)
else: exit('The file does not have a token, please open token_bot.txt and check its integrity.')

@bot.message_handler(commands=['start', 'help'])
def commands_bot(msg):
    if msg.text == '/start' or '/help':
        name = msg.from_user.first_name
        response = f'Hello {name}!\nChoose your language to start using this bot;'
        bot.send_message(msg.chat.id, response)
        markup = types.InlineKeyboardMarkup(row_width=2)
        for language in langs.keys():
            sleep(1)
            button = types.InlineKeyboardButton(language, callback_data=language)
            markup.add(button)

@bot.callback_query_handler(func=lambda call: call.data in langs.keys())
def define_lang(call):
    lang_code = call.data
    user_id = call.from_user.id
    user_name = call.from_user.first_name
    bot.send_message(call.chat.id, langs[lang_code])
    save_user(user_name, user_id, lang_code)

# @bot.message_handler(func=lambda msg: len(msg.text) >5)
#def audioGeneration(msg):
    

try:
    bot.polling()
    print('Bot online!')
except Exception as x:
    log.critical('Exit code: '+str(x))
    exit('O bot caiu, motivo: '+str(x))