# diaseduardo139@gmail.com
import os
import json
import logging as log
from random import randint
from time import sleep
from telebot import TeleBot, types
from gtts import gTTS
log.basicConfig(level=log.ERROR, filename='bot_log.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

langs = {
    'pt-br': 'Olá! 🌟 Seu idioma foi definido com sucesso para Português (Brasil). Agora pode escrever à vontade. 😊',
    'pt': 'Olá! 🌟 Seu idioma foi definido com sucesso para Português. Agora pode escrever à vontade. 😊',
    'en': 'Hello! 🌟 Your language has been successfully set to English. You can start writing freely. 😊',
    'es': '¡Hola! 🌟 Tu idioma se ha configurado con éxito como Español. Ahora puedes comenzar a escribir a tus anchas. 😊',
    'tr': 'Merhaba! 🌟 Diliniz başarıyla Türkçe olarak ayarlandı. Artık özgürce yazmaya başlayabilirsiniz. 😊',
    'fr': 'Bonjour ! 🌟 Votre langue a été configurée avec succès en français. Vous pouvez maintenant commencer à écrire librement. 😊',
    'ru': 'Привет! 🌟 Ваш язык успешно установлен как русский. Теперь вы можете начать писать на свободу. 😊',
    'de': 'Hallo! 🌟 Ihre Sprache wurde erfolgreich auf Deutsch festgelegt. Jetzt können Sie frei zu schreiben beginnen. 😊',
    'ja': 'こんにちは！ 🌟 言語が日本語に正常に設定されました。これで自由に書き始めることができます。 😊',
    'zh': '你好！ 🌟 您的语言已成功设置为中文。现在您可以自由地开始写作。 😊'
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
        log.critical('Could not save file %s' % x)

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

def delete_user(user_id):
    filename = "users.json"
    try:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                if str(user_id) in data:
                    del data[str(user_id)]
                else:
                    return 'There are no saved preferences, nothing to reset.'
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            return 'I successfully reset your settings to default.'
    except Exception as x:
        log.error("Error deleting user: %s" % x)
        return 'There are no saved preferences, nothing to reset.'

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

token_bot = get_token_bot()
if token_bot:
    bot = TeleBot(token_bot)
else:
    log.error('Token bot not found in file')
    exit('The file does not have a token, please open token_bot.txt and check its integrity.')

button_id = None # save the id buttons
def keyboard_buttons(msg):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for language in langs.keys():
        button = types.InlineKeyboardButton(language, callback_data=language)
        markup.add(button)
    buttons = bot.send_message(msg.chat.id, 'Choose your preferred language:', reply_markup=markup)
    return buttons.message_id

@bot.message_handler(commands=['start', 'reset'])
def commands_bot(msg):
    name = msg.from_user.first_name
    global button_id
    if msg.text == '/start':
        response = f'Hello {name}, this bot converts text messages into audio. Just select your language and get started.\nTo reset your language, type /reset.'
    elif msg.text == '/reset':
        response = delete_user(msg.from_user.id)
    bot.send_message(msg.chat.id, response)
    if get_user(msg.from_user.id) == None:
        button_id = keyboard_buttons(msg)

@bot.callback_query_handler(func=lambda call: call.data in langs.keys())
def config_per_button(call):
    lang_code = call.data
    user_id = call.from_user.id
    user_name = call.from_user.first_name
    if button_id:
        bot.delete_message(call.message.chat.id, button_id)
        bot.send_message(call.message.chat.id, langs[lang_code])
    else:
        bot.send_message(call.message.chat.id, '⚠ Error, please clear the conversation history with me so that everything works normally.')
        log.error("I couldn't delete the message with the buttons, I asked the user to clear the conversation.")
    if user_name and user_id and lang_code:
        save_user(user_name, user_id, lang_code)

@bot.message_handler(func=lambda msg: len(msg.text) >5)
def generation(msg):
    global button_id
    user_id = msg.from_user.id
    lang_user = get_user(user_id)
    if lang_user:
        audio = TTS(msg.text, lang_user)
        if audio:
            send_audio(msg.chat.id, audio, msg.text)
            delete_audio(audio)
    
    else:
        # choose the language
        button_id = keyboard_buttons(msg)

if __name__ == '__main__':
    try:
        print('Bot online!')
        bot.polling()
        print('Bot offline...')
    except Exception as x:
        log.critical('broken code: '+str(x))
        exit('bot crashed, reason: %s' %x)
        