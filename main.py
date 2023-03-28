import os
import zipfile
from uuid import uuid4
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = "YOUR_BOT_TOKEN_HERE"
TEMP_DIR = "temp"

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

file_dict = {}
is_zipping = False

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Send me the /zip command to start zipping files.")

def handle_files(update: Update, context: CallbackContext):
    global is_zipping
    if is_zipping:
        file_id = update.message.document.file_id
        file_name = update.message.document.file_name
        unique_id = str(uuid4())
        file_dict[unique_id] = {'file_id': file_id, 'file_name': file_name}
        update.message.reply_text(f"File received. Reference ID: {unique_id}")
    else:
        update.message.reply_text("Please send the /zip command first.")

def zip_command(update: Update, context: CallbackContext):
    global is_zipping
    is_zipping = True
    update.message.reply_text("Send me the files you want to zip. Once you're done, send the /stopzip command.")

def stopzip_command(update: Update, context: CallbackContext):
    global is_zipping
    is_zipping = False
    zip_file_name = f"{TEMP_DIR}/zipped_{uuid4()}.zip"

    with zipfile.ZipFile(zip_file_name, 'w') as zf:
        for unique_id, file_info in file_dict.items():
            file_id = file_info['file_id']
            file_name = file_info['file_name']
            file = context.bot.get_file(file_id)
            file.download(f"{TEMP_DIR}/{file_name}")
            zf.write(f"{TEMP_DIR}/{file_name}", file_name)
            os.remove(f"{TEMP_DIR}/{file_name}")

    with open(zip_file_name, 'rb') as zf:
        context.bot.send_document(chat_id=update.effective_chat.id, document=InputFile(zf), filename="zipped_files.zip")

    os.remove(zip_file_name)
    file_dict.clear()

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document, handle_files))
    dp.add_handler(CommandHandler("zip", zip_command))
    dp.add_handler(CommandHandler("stopzip", stopzip_command))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()