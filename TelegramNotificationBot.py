import json
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes
from telegram.ext import filters


DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
ADMIN_MESSAGES_FILE = os.path.join(os.path.dirname(__file__), "admin_messages.json")


data = {"subscribers": {}, "messages": []}
admin_messages = []


def load_data():
    global data, admin_messages
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            print("User information and messages have been loaded successfully.")
    except FileNotFoundError:
        print("File data.json not found. Data starts empty")
        data = {"subscribers": {}, "messages": []}

    try:
        with open(ADMIN_MESSAGES_FILE, "r") as file:
            admin_messages = json.load(file)
            print("Admin messages successfully loaded.")
    except FileNotFoundError:
        print("File admin_messages.json not found. Starting empty admin message list.")
        admin_messages = []


def save_data():
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            print("User information and messages saved.")
    except Exception as e:
        print(f"Error saving data.json: {e}")

    try:
        with open(ADMIN_MESSAGES_FILE, "w") as file:
            json.dump(admin_messages, file, ensure_ascii=False, indent=4)
            print("Admin messages saved.")
    except Exception as e:
        print(f"Error saving admin_messages.json: {e}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = str(update.effective_chat.id)
    username = update.effective_user.username if update.effective_user.username else "Uncertain"


    data["subscribers"][chat_id] = username
    save_data()

    print(f"Added user: {chat_id} - {username}")
    await update.message.reply_text("Hello! You have been added to the notification list.")


async def send_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat.id != YOUR_ADMIN_ID:
        await update.message.reply_text("Only admin can do this.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("Please enter the command correctly:\n/sendto <id> <message text>")
        return

    try:
        user_id = int(context.args[0])
        message = " ".join(context.args[1:])

        await context.bot.send_message(chat_id=user_id, text=message)
        print(f"Message sent to {user_id}: {message}")
        await update.message.reply_text(f"Message sent to user {user_id}.")
    except ValueError:
        await update.message.reply_text("ID must be a number.")
    except Exception as e:
        print(f"Error sending message: {e}")
        await update.message.reply_text(f"Error sending message: {e}")


async def send_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    username = update.effective_user.username if update.effective_user.username else "unknown"
    message = update.message.text.replace("@sendToAdmin", "").strip()

    if not message:
        await update.message.reply_text("Please enter your message after @sendToAdmin.")
        return


    admin_messages.append({"chat_id": chat_id, "username": username, "message": message})
    save_data()


    admin_message = f"New message from user:\nID: {chat_id}\nUsername: @{username}\nMessage text: {message}"
    await context.bot.send_message(chat_id=YOUR_ADMIN_ID, text=admin_message)

    print(f"Received message from {chat_id}: {message}")
    await update.message.reply_text("Your message has been received and sent to the admin.")


async def list_subscribers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat.id != YOUR_ADMIN_ID:
        await update.message.reply_text("Only admin can do this.")
        return

    if not data["subscribers"]:
        await update.message.reply_text("No user registered.")
        return

    user_list = "\n".join([f"id: {chat_id}, username: @{username}" for chat_id, username in data["subscribers"].items()])
    await update.message.reply_text(f"user list:\n{user_list}")


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat.id != YOUR_ADMIN_ID:
        await update.message.reply_text("Only admin can do this.")
        return

    if len(context.args) == 0:
        await update.message.reply_text("Please enter message text:\n/broadcast <message text>")
        return

    message = " ".join(context.args)

    for chat_id in data["subscribers"]:
        try:
            await context.bot.send_message(chat_id=int(chat_id), text=message)
        except Exception as e:
            print(f"Error sending message to {chat_id}: {e}")

    await update.message.reply_text("The message has been sent to all users.")


def main():
    load_data()
    application = Application.builder().token("BOT_TOKEN").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("sendto", send_to_user))
    application.add_handler(CommandHandler("subscribers", list_subscribers))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(MessageHandler(filters.Regex(r"@sendToAdmin"), send_to_admin))

    application.run_polling()

if __name__ == '__main__':
    YOUR_ADMIN_ID = 1234567  # Admin Id
    main()
