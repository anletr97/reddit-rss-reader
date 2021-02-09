"""This module will process telegram bot method"""
import telegram
from constant import BOT_TOKEN, CHAT_ID

bot = telegram.Bot(BOT_TOKEN)


def send_message(message):
    '''Handle sending message'''
    bot.send_message(CHAT_ID, message)
