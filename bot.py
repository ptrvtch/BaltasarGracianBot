import os
from telegram.ext import Updater, CommandHandler
import logging
import random

bot_token = os.environ.get("bot_token")


logger = logging.getLogger(__name__)

def main():
    quotes = open("baltasar.txt", "r", encoding="utf8")
    system_random = random.SystemRandom()
    data = quotes.readlines()
    updater = Updater(token=bot_token, use_context=True)

    dispatcher = updater.dispatcher

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    def start(update, context):
        logger.info("Start command")
        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text="Добро пожаловать! Нажмите /quote чтобы получить цитату из книги",
        )

    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)

    def quote(update, context):
        message = system_random.choice(data)
        try:
            context.bot.sendMessage(
                chat_id=update.message.chat_id, text=message, parse_mode="Markdown"
            )
            # logging.info(flatten_metadata(update.message))
            logger.info({"message": message[0:20]})
        except Exception as e:
            logger.warning(str(e))
            context.bot.sendMessage(
                chat_id=update.message.chat_id, text=message, parse_mode="Markdown"
            )

    quote_handler = CommandHandler("quote", quote)
    dispatcher.add_handler(quote_handler)

    updater.start_polling()
    logger.info("Bot is ready!")
    updater.idle()


if __name__ == "__main__":
    main()
