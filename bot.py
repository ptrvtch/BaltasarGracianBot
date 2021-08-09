import os
from telegram.ext import Updater, CommandHandler
import logging
import random
import requests

bot_token = os.environ.get("BOT_TOKEN")
GA_TRACKING_ID = os.environ.get("GA_TRACKING_ID")

logger = logging.getLogger(__name__)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def track_event(cid, category, action, label=None, value=0):
    data = {
        'v': '1',  # API Version.
        'tid': GA_TRACKING_ID,  # Tracking ID / Property ID.
        # Anonymous Client Identifier. Ideally, this should be a UUID that
        # is associated with particular user, device, or browser instance.
        'cid': cid,
        't': 'event',  # Event hit type.
        'ec': category,  # Event category.
        'ea': action,  # Event action.
        'el': label,  # Event label.
        'ev': value,  # Event value, must be an integer
        'ua': 'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14'
    }

    response = requests.post(
        'https://www.google-analytics.com/collect', data=data)

    response.raise_for_status()


def main():
    quotes = open("baltasar.txt", "r", encoding="utf8")
    system_random = random.SystemRandom()
    data = quotes.readlines()
    updater = Updater(token=bot_token, use_context=True)

    dispatcher = updater.dispatcher


    def start(update, context):
        logger.info("Start command")
        chat_id = update.message.chat_id
        if GA_TRACKING_ID:
            track_event(update.message.chat_id, 'start', '(not set)')
        context.bot.sendMessage(
            chat_id=chat_id,
            text="Добро пожаловать! Нажмите /quote чтобы получить цитату из книги",
        )

    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)

    def quote(update, context):
        message = system_random.choice(data)
        chat_id = update.message.chat_id
        if GA_TRACKING_ID:
            track_event(update.message.chat_id, 'quote', message[0:20])
        try:
            context.bot.sendMessage(
                chat_id=chat_id, text=message, parse_mode="Markdown"
            )
            # logging.info(flatten_metadata(update.message))
            logger.info(context)
            logger.info({"message": message[0:20]})
        except Exception as e:
            logger.warning(str(e))
            context.bot.sendMessage(
                chat_id=chat_id, text=message, parse_mode="Markdown"
            )

    quote_handler = CommandHandler("quote", quote)
    dispatcher.add_handler(quote_handler)

    updater.start_polling()
    logger.info("Bot is ready!")
    updater.idle()


if __name__ == "__main__":
    main()
