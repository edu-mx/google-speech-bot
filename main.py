# diaseduardo139@gmail.com
import os
from random import randint as rand
import telebot

# token in token_bot.txt
def get_token_bot(filename='token_bot.txt'):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            token = file.read().strip()
            return token
    except FileNotFoundError:
        print('The token_bot.txt file does not exist, create it and add the bot token there;')
        return
    finally:
        file.close()

token_bot = get_token_bot()
bot = telebot.TeleBot(token_bot)
get_token_bot()