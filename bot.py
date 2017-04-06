from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import datetime
import logging
import pprint
import random
import botan


def main():
    botan_token = 'd8e83502-a500-42e6-9f2d-10372d5548e2'
    quotes = open("baltasar.txt", 'r', encoding='utf8')
    system_random = random.SystemRandom()
    data = quotes.readlines()
    updater = Updater(token='331914717:AAEOP8yEUjlks91WS9sJyHGhN7lPhnyvyb4')

    dispatcher = updater.dispatcher

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
        level=logging.INFO
    )

    def start(bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text="Добро пожаловать! Нажмите /quote чтобы получить цитату из книги")

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    def quote(bot, update):
        message = system_random.choice(data)
        try:
            bot.sendMessage(chat_id=update.message.chat_id, text=message, parse_mode='Markdown')
            print(botan.track(botan_token, update.message.from_user.id, message))
        except Exception as e:
            print('Exception:' + e)

    quote_handler = CommandHandler('quote', quote)
    dispatcher.add_handler(quote_handler)

    updater.start_polling()
    print('Bot is ready!')
    updater.idle()

if __name__ == '__main__':
    main()