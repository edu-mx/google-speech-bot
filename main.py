# diaseduardo139@gmail.com
import os
import json
import logging as log
from random import randint
from time import sleep
from telebot import TeleBot, types
from gtts import gTTS
log.basicConfig(level=log.ERROR, filename='bot_log.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

# language codes
langs = {
    'pt-br': 'Olá! 🌟 Seu idioma foi definido como Português (Brasil). Tudo pronto para começar a escrever! 🎉 Digite /help para mais ajuda.',
    'pt': 'Olá! 🌟 Seu idioma foi definido como Português. Tudo pronto para começar a escrever! 🎉 Digite /help para mais ajuda.',
    'en': 'Hello! 🌟 Your language has been set to English. All set to start typing! 🎉 Type /help for more assistance.',
    'es': '¡Hola! 🌟 Se ha establecido tu idioma como Español. ¡Listo para comenzar a escribir! 🎉 Escribe /help para obtener más ayuda.',
    'tr': 'Merhaba! 🌟 Diliniz Türkçe olarak ayarlandı. Yazmaya başlamak için hazırsınız! 🎉 Daha fazla yardım için /help yazabilirsiniz.',
    'fr': 'Bonjour ! 🌟 Votre langue a été définie comme le Français. Tout est prêt pour commencer à écrire ! 🎉 Tapez /help pour plus d\'assistance.',
    'ru': 'Привет! 🌟 Ваш язык был установлен как Русский. Всё готово, чтобы начать писать! 🎉 Введите /help для получения дополнительной помощи.',
    'de': 'Hallo! 🌟 Ihre Sprache wurde auf Deutsch festgelegt. Alles bereit, um mit dem Schreiben zu beginnen! 🎉 Geben Sie /help für weitere Unterstützung ein.',
    'ja': 'こんにちは！ 🌟 言語が日本語に設定されました。書き始める準備が整いました！ 🎉 詳細なヘルプは /help と入力してください。',
    'zh': '你好！ 🌟 您的语言已设置为中文。一切就绪，可以开始输入了！ 🎉 输入 /help 获取更多帮助。'
}

# the token is in token_bot.txt
def get_token_bot(filename='token_bot.txt'):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            token = file.read().strip()
            return token
    except FileNotFoundError as x:
        log.error('Token not found %s' % x)
        exit('The token_bot.txt file does not exist, create it and add the bot token there;')

def TTS(text_voice='1, 2, 3.', lang_voice='en'):
    try:
        tts_voice = gTTS(text_voice, lang=lang_voice)
        folder = 'files'
        audioTempFile = f'{folder}/Audio_{randint(100, 999)}_{lang_voice}.mp3'
        if not os.path.exists(folder):
            os.makedirs(folder)
        tts_voice.save(audioTempFile)
        return audioTempFile
    except Exception as x:
        log.critical('Não foi possível salvar o arquivo %s' % x)
        return

def send_audio(chat_id, filename, description):
    try:
        short_desc = f'{description[:40]}...'
        with open(filename, 'rb') as audio:
            bot.send_audio(chat_id, audio, caption=short_desc)
    except Exception as x:
        log.error('Unable to send audio %S. %S' %(filename, x))

def delete_audio(file):
    try:
        if os.path.exists(file):
            os.remove(file)
    except Exception as x:
        log.critical('Could not delete file %s, reason: ' %(file, x))

def save_user(name, user_id, lang):
    user_data = {
        "name": name,
        "user_id": user_id,
        "lang": lang
    }
    filename = "users.json"
    try:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                if str(user_id) not in data:
                    data[str(user_id)] = user_data
        else:
            data = {str(user_id): user_data}

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    except Exception as x:
        log.error("Error saving user: %s" % x)

def get_user(user_id):
    filename = "users.json"
    try:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                if str(user_id) in data:
                    return data[str(user_id)]["lang"]
    except Exception as x:
        log.error('Error getting user: %s' % x)
        return

token_bot = get_token_bot()
if token_bot:
    bot = TeleBot(token_bot)
else:
    log.error('Token bot not found in file')
    exit('The file does not have a token, please open token_bot.txt and check its integrity.')

buttons_info = None
@bot.message_handler(commands=['start', 'help'])
def commands_bot(msg):
    global buttons_info
    name = msg.from_user.first_name
    if msg.text == '/start':
        response = f'Hello {name}!\nChoose your language to start using this bot;'
    elif msg.text == '/help':
        response = 'This bot converts text to speech. To start, just type a text and send, if your language is not defined, a request will be sent for you to choose yours.'
    bot.send_message(msg.chat.id, response)
    markup = types.InlineKeyboardMarkup(row_width=2)
    for language in langs.keys():
        button = types.InlineKeyboardButton(language, callback_data=language)
        markup.add(button)
    buttons = bot.send_message(msg.chat.id, 'Select your language:', reply_markup=markup)
    buttons_info = buttons.message_id

@bot.callback_query_handler(func=lambda call: call.data in langs.keys())
def config_per_button(call):
    lang_code = call.data
    user_id = call.from_user.id
    user_name = call.from_user.first_name
    if buttons_info: # if saved the id of the buttons
        bot.delete_message(call.message.chat.id, buttons_info)
        bot.send_message(call.message.chat.id, langs[lang_code])
    else:
        bot.send_message(call.message.chat.id, '⚠ Error, please clear the conversation history with me so that everything works normally.')
        log.error("I couldn't delete the message with the buttons, I asked the user to clear the conversation.")
    if user_name and user_id and lang_code:
        save_user(user_name, user_id, lang_code)

@bot.message_handler(func=lambda msg: len(msg.text) >5)
def generation(msg):
    user_id = msg.from_user.id
    lang_user = get_user(user_id)
    if lang_user:
        audio = TTS(msg.text, lang_user)
        if audio:
            send_audio(msg.chat.id, audio, msg.text)
            delete_audio(audio)

if __name__ == '__main__':
    try:
        print('Bot online!')
        bot.polling()
        print('Bot offline...')
    except Exception as x:
        log.critical('Exit code: '+str(x))
        exit('O bot caiu, motivo: %s' %x)