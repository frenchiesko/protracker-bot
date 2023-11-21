import telebot
from telebot import types

import os
from dotenv import load_dotenv


load_dotenv('.env')
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)


# FUNCTION - Main Keyboard markup
def create_markup(language):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if language == 'Russian':
        btn1 = types.KeyboardButton('🆕 Новая задача')
        btn2 = types.KeyboardButton('📄 Мои задачи')
        btn3 = types.KeyboardButton('📖Рассмотреть задачу')
        btn4 = types.KeyboardButton('❌ Удалить задачу')
        btn5 = types.KeyboardButton('📊 Аналитика')
        btn6 = types.KeyboardButton('❓ Пройти опрос')
        btn7 = types.KeyboardButton("👀 О боте")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    elif language == 'English':
        btn1 = types.KeyboardButton('🆕 New task')
        btn2 = types.KeyboardButton('📄 My tasks')
        btn3 = types.KeyboardButton('📖 Task info')
        btn4 = types.KeyboardButton('❌ Delete task')
        btn5 = types.KeyboardButton('📊 Analytics')
        btn6 = types.KeyboardButton('❓ Take a survey')
        btn7 = types.KeyboardButton("👀 About bot")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    return markup


# TASK CLASS - another survey about new task
class TaskSurvey:

    def __init__(self):
        pass

    def question_one(self, message, lang):
        if lang == 'Russian':
            bot.send_message(message.from_user.id,
                             "🗓️ Дата начала выполнения вашей задачи\nПример - 18 Ноября")
        elif lang == 'English':
            bot.send_message(message.from_user.id,
                             "🗓️ Date to start your task\nExample - November 18th")

    def question_two(self, message, lang):
        if lang == 'Russian':
            bot.send_message(message.from_user.id,
                             "📝 Дайте название вашей задачи")
        elif lang == 'English':
            bot.send_message(message.from_user.id,
                             "📝 Give a title to your task")

    def question_three(self, message, lang):
        if lang == 'Russian':
            bot.send_message(message.from_user.id,
                             "📄 Дайте краткое описание вашей задачи")
        elif lang == 'English':
            bot.send_message(message.from_user.id,
                             "📄 Provide a brief description of your task")

    def question_four(self, message, lang):
        if lang == 'Russian':
            bot.send_message(message.from_user.id,
                             "🔗 Материалы и ресурсы для выполнения задачи (url, и т.д)")
        elif lang == 'English':
            bot.send_message(message.from_user.id,
                             "🔗 Materials and resources for task completion (URLs, etc.)")

    def question_five(self, message, lang):
        if lang == 'Russian':
            markup = types.ReplyKeyboardMarkup(row_width=1)
            btn1 = types.KeyboardButton("🟢 Высокий")
            btn2 = types.KeyboardButton("🟡 Средний")
            btn3 = types.KeyboardButton("🔴 Низкий")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id,
                             "⚡ Укажите приоритет задачи", reply_markup=markup)
        elif lang == 'English':
            markup = types.ReplyKeyboardMarkup(row_width=1)
            btn1 = types.KeyboardButton("🟢 High")
            btn2 = types.KeyboardButton("🟡 Medium")
            btn3 = types.KeyboardButton("🔴 Low")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id,
                             "⚡ Indicate the priority of the task", reply_markup=markup)

    def question_six(self, message, lang):
        if lang == 'Russian':
            markup = types.ReplyKeyboardMarkup(row_width=1)
            btn1 = types.KeyboardButton("⚡️ Сегодня")
            btn2 = types.KeyboardButton("💭 В течение дня")
            btn3 = types.KeyboardButton("🤷 Отложено")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id,
                             "⏳ Когда приступаете к задаче?", reply_markup=markup)
        elif lang == 'English':
            markup = types.ReplyKeyboardMarkup(row_width=1)
            btn1 = types.KeyboardButton("⚡️ Today")
            btn2 = types.KeyboardButton("💭 During the day")
            btn3 = types.KeyboardButton("🤷 Unknown")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id,
                             "⏳ When do you start the task?", reply_markup=markup)

    def question_seven(self, message, lang):
        if lang == 'Russian':
            markup = types.ReplyKeyboardMarkup(row_width=1)
            btn1 = types.KeyboardButton("Да")
            btn2 = types.KeyboardButton("Нет")
            markup.add(btn1, btn2)
            bot.send_message(message.from_user.id,
                             "👥 Планируете делать самостоятельно?", reply_markup=markup)
        elif lang == 'English':
            markup = types.ReplyKeyboardMarkup(row_width=1)
            btn1 = types.KeyboardButton("Yes")
            btn2 = types.KeyboardButton("No")
            markup.add(btn1, btn2)
            bot.send_message(message.from_user.id,
                             "👥 Planning to do it independently?", reply_markup=markup)

    def question_eight(self, message, lang):
        if lang == 'Russian':
            bot.send_message(message.from_user.id,
                             "🌟 Оцените уровень сложности от 1 до 10\nВведите число:", reply_markup=create_markup(lang))
        elif lang == 'English':
            bot.send_message(message.from_user.id,
                             "🌟 Rate the difficulty level from 1 to 10\nPlease write a number:", reply_markup=create_markup(lang))

    @bot.message_handler(commands=['new_task'])
    def start_new_task(self, message, lang):
        self.question_one(message, lang)
