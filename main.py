import telebot

API_TOKEN = '7669462188:AAENuSv4SfwbriruokIpVoORSd_e1DslxDQ'
ADMIN_ID = 1121163791 

bot = telebot.TeleBot(API_TOKEN)

user_queries = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
 welcome_text = "Добро пожаловать! Я бот, который поможет вам связаться с администратором. Напишите ваше сообщение, и я передам его."
 bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: message.from_user.id != ADMIN_ID)
def handle_user_message(message):
    user_queries[message.from_user.id] = message.text
    bot.send_message(ADMIN_ID, f"Сообщение от {message.from_user.username}: {message.text}")
    bot.reply_to(message, "Ваше сообщение отправлено администратору.")

@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID)
def handle_admin_response(message):
    if user_queries:
        user_id = next(iter(user_queries))
        try:
            bot.send_message(user_id, f"Ответ от админа: {message.text}")
            bot.reply_to(message, f"Ответ отправлен пользователю с ID {user_id}.")
            del user_queries[user_id]
        except Exception as e:
            print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")
    else:
        bot.reply_to(message, "Нет пользователей с вопросами.")

if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)
