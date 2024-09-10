from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from telegram.ext import filters  # Changed this line
from PIL import Image, ImageFilter
import io

TOKEN = '6993238792:AAHkzUgU5a0_L5ANOqzZICvBNvmASnRky4E'  # আপনার বট টোকেন এখানে দিন
CHANNEL_ID = '@photo_drawing_editor'  # আপনার চ্যানেলের ইউজারনেম এখানে দিন

def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    context.bot.send_message(
        chat_id=user_id,
        text="Welcome! Please join our channel to use this bot: " + CHANNEL_ID
    )

def check_channel_membership(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id

    try:
        member = context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        else:
            context.bot.send_message(
                chat_id=user_id,
                text="You need to join our channel to use this bot: " + CHANNEL_ID
            )
            return False
    except Exception as e:
        context.bot.send_message(
            chat_id=user_id,
            text="Error checking channel membership. Please try again later."
        )
        print(f"Error: {e}")
        return False

def photo(update: Update, context: CallbackContext):
    if not check_channel_membership(update, context):
        return

    file = update.message.photo[-1].get_file()
    file.download('received_photo.jpg')

    # Open the image file
    with Image.open('received_photo.jpg') as img:
        # Example: Apply a filter
        img = img.filter(ImageFilter.CONTOUR)

        # Save edited image
        output = io.BytesIO()
        img.save(output, format='JPEG')
        output.seek(0)

    # Send back the edited photo
    update.message.reply_photo(photo=InputFile(output, filename='edited_photo.jpg'))

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(filters.PHOTO, photo))  # Updated this line

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
