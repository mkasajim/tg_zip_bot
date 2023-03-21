import os
import zipfile
from telegram.ext import Updater, CommandHandler


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! Send me the files you want to zip.")


def zip_files(update, context):
    files = context.bot.get_file(update.message.document.file_id)
    filename = update.message.document.file_name.split('.')[0] + '.zip'
    with open(filename, 'wb') as f:
        f.write(files.download_as_bytearray())

    context.bot.send_document(chat_id=update.effective_chat.id, document=open(filename, 'rb'))
    os.remove(filename)


def main():
    updater = Updater('YOUR_TELEGRAM_BOT_TOKEN', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('zip', zip_files))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
