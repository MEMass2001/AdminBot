import telebot
import time

bot = telebot.TeleBot('7195560279:AAE8iKWhwRLVv5iiw0P7pRWSM6UE58an2gA')

stats = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом. Напиши /help, чтобы узнать, что я умею.")

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, """/kick - кикнуть пользователя\n/mute - замутить пользователя на определенное время\n/unmute - размутить пользователя\n/stats - показать статистику чата\n/selfstat - показать свою статистику""")

@bot.message_handler(commands=['kick'])
def kick_user(message):
    chat_id = message.chat.id
    sender_status = bot.get_chat_member(chat_id, message.from_user.id).status

    if sender_status == 'administrator' or sender_status == 'creator':
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            user_status = bot.get_chat_member(chat_id, user_id).status
            if user_status == 'administrator' or user_status == 'creator':
                bot.reply_to(message, "Невозможно кикнуть администратора.")
            else:
                bot.kick_chat_member(chat_id, user_id)
                bot.reply_to(message, f"Пользователь {message.reply_to_message.from_user.username} был кикнут.")
        else:
            bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите кикнуть.")
    else:
        bot.reply_to(message, "Для выполнения команды вы должны иметь права администратора в чате")

@bot.message_handler(commands=['mute'])
def mute_user(message):
    chat_id = message.chat.id
    sender_status = bot.get_chat_member(chat_id, message.from_user.id).status

    if sender_status == 'administrator' or sender_status == 'creator':
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            user_status = bot.get_chat_member(chat_id, user_id).status
            if user_status == 'administrator' or user_status == 'creator':
                bot.reply_to(message, "Невозможно замутить администратора.")
            else:
                duration = 60
                args = message.text.split()[1:]
                if args:
                    try:
                        duration = int(args[0])
                    except ValueError:
                        bot.reply_to(message, "Неправильный формат времени.")
                        return
                    if duration <= 0:
                        bot.reply_to(message, "Время должно быть больше нуля.")
                        return
                bot.restrict_chat_member(chat_id, user_id, until_date=time.time()+duration*60)
                bot.reply_to(message, f"Пользователь {message.reply_to_message.from_user.username} замучен на {duration} минут.")
        else:
            bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите замутить.")
    else:
        bot.reply_to(message, "Для выполнения команды вы должны иметь права администратора в чате")

@bot.message_handler(commands=['unmute'])
def unmute_user(message):
    chat_id = message.chat.id
    sender_status = bot.get_chat_member(chat_id, message.from_user.id).status

    if sender_status == 'administrator' or sender_status == 'creator':
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            bot.restrict_chat_member(chat_id, user_id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)
            bot.reply_to(message, f"Пользователь {message.reply_to_message.from_user.username} размучен.")
        else:
            bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите размутить.")
    else:
        bot.reply_to(message, "Для выполнения команды вы должны иметь права администратора в чате")

@bot.message_handler(commands=['stats'])
def chat_stats(message):
    chat_id = message.chat.id
    if chat_id not in stats:
        bot.reply_to(message, "Статистика чата пуста.")
    else:
        total_messages = stats[chat_id]['total_messages']
        unique_users = len(stats[chat_id]['users'])
        bot.reply_to(message, f"Статистика чата:\nВсего сообщений: {total_messages}\nУникальных пользователей: {unique_users}")

@bot.message_handler(commands=['selfstat'])
def user_stats(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    if chat_id not in stats:
        bot.reply_to(message, "Статистика чата пуста.")
    else:
        if user_id not in stats[chat_id]['users']:
            bot.reply_to(message, "Вы еще не отправляли сообщений в этом чате.")
        else:
            user_messages = stats[chat_id]['users'][user_id]['messages']
            total_messages = stats[chat_id]['total_messages']
            percentage = round(user_messages / total_messages * 100, 2)
            bot.reply_to(message, f"Статистика для пользователя @{username}:\nВсего сообщений: {user_messages}\nПроцент от общего количества сообщений: {percentage}%")

@bot.message_handler(func=lambda message: True)
def count_message(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if chat_id not in stats:
        stats[chat_id] = {
            'total_messages': 0,
            'users': {}
        }
    if user_id not in stats[chat_id]['users']:
        stats[chat_id]['users'][user_id] = {
            'messages': 0
        }

    stats[chat_id]['total_messages'] += 1
    stats[chat_id]['users'][user_id]['messages'] += 1

    print(stats)

if __name__ == "__main__":
    print('Я проснулся!')
    bot.infinity_polling(none_stop=True)