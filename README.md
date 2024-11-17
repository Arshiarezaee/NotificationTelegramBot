# 🤖 Telegram Notification Bot

A **Telegram Bot** for managing user communications, broadcasting messages, and connecting users with the admin seamlessly. It’s designed to handle user registration, direct messaging, and logging user data in a persistent storage format.

---

## ✨ Features

- **User Registration**: Automatically registers users when they start the bot.
- **Broadcasting**: Allows the admin to send messages to all registered users.
- **Private Messaging**: Admin can send direct messages to a specific user.
- **User-to-Admin Messaging**: Users can send messages directly to the admin with the `@sendToAdmin` command.
- **Persistent Storage**: All user data and messages are stored in JSON files to ensure data is retained after restarting the bot.
- **Admin Notifications**: Sends all user messages to the admin with their Telegram ID and username.

---

## 🛠️ How It Works

1. **User Registration**:
   - When a user interacts with the bot for the first time using `/start`, their Telegram ID and username are saved in the database.
   
2. **Broadcasting**:
   - The admin can use the `/broadcast <message>` command to send a message to all registered users.
   
3. **Direct Messaging**:
   - Admins can use the `/sendto <user_id> <message>` command to send a private message to a specific user.
   
4. **User-to-Admin Communication**:
   - Users can use the `@sendToAdmin <message>` command to send a message to the admin, which includes their ID and username.
   
5. **Persistent Data**:
   - All user information and messages are stored in `data.json`, while messages sent to the admin are logged in `admin_messages.json`.

---

## 📜 Bot Commands

| Command                | Access Level | Description                                                                 |
|-------------------------|--------------|-----------------------------------------------------------------------------|
| `/start`               | All Users    | Registers the user in the bot's database.                                   |
| `/subscribers`         | Admin Only   | Displays a list of all registered users (ID and username).                  |
| `/broadcast <message>` | Admin Only   | Sends a broadcast message to all registered users.                          |
| `/sendto <user_id> <message>` | Admin Only | Sends a private message to a specific user.                                 |
| `@sendToAdmin <message>` | All Users  | Sends a message to the admin with the user's ID and username attached.      |

---

## 📦 Requirements

- **Python**: Version 3.8 or higher
- **Libraries**:
  - `python-telegram-bot` (Install via `pip install python-telegram-bot`)

---

## 🚀 Installation

Follow these steps to set up and run the bot:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/telegram-notification-bot.git
   cd telegram-notification-bot
