import telebot
from telebot import types

import os
from dotenv import load_dotenv

load_dotenv('.env')
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)


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


# SURVEY CLASS - list of questions
class SurveyClass:

    def __init__(self):
        pass

    def question_one(self, message, lang):
        if lang == 'English':
            bot.send_message(message.from_user.id,
                             "Rate the complexity of your typical work day on a scale of 1 to 10, where 1 is very easy,"
                             "and 10 is very difficult."
                             "\n\nPlease consider the variety of tasks you encounter.")
        elif lang == 'Russian':
            bot.send_message(message.from_user.id,
                             "Оцените уровень сложности вашего обычного рабочего дня по шкале от 1 до 10, "
                             "где 1 - очень"
                             " легкий, 10 - очень сложный.\n\n"
                             "Пожалуйста, учтите разнообразие задач, с которыми вы сталкиваетесь")

    def question_one_hard(self, message, lang):
        if lang == 'English':
            bot.send_message(message.from_user.id,
                             "Rate the complexity of your most difficult work day on a scale of 1 to 10, where 1 is "
                             "very easy,"
                             "and 10 is very difficult."
                             "\n\nPlease consider the variety of tasks you encounter.")
        elif lang == 'Russian':
            bot.send_message(message.from_user.id,
                             "Оцените уровень сложности вашего самого сложного рабочего дня по шкале от 1 до 10, "
                             "где 1 - очень"
                             " легкий, 10 - очень сложный.\n\n"
                             "Пожалуйста, учтите разнообразие задач, с которыми вы сталкиваетесь")

    def question_two(self, message, lang):
        if lang == 'English':
            bot.send_message(message.from_user.id,
                             "Rate you typical task complexity on a scale from 1 to 10, where 1 is very easy and 10 "
                             "is very difficult"
                             "from 1 to 10.")
        elif lang == 'Russian':
            bot.send_message(message.from_user.id,
                             "Оцените уровень сложности вашей обычной задачи, оцените "
                             "уровень сложности от 1 до 10")

    def question_two_hard(self, message, lang):
        if lang == 'English':
            bot.send_message(message.from_user.id,
                             "Imagine a challenging task. How would you rate its complexity on a scale from 1 to 10, "
                             "where 1 is very easy and 10 is very difficult?")
        elif lang == 'Russian':
            bot.send_message(message.from_user.id,
                             "Представьте самую сложную для вас задачу. Насколько бы вы оценили её сложность по шкале "
                             "от 1 до 10,"
                             "где 1 - очень легко, а 10 - очень сложно?")

    def question_three(self, message, lang):
        if lang == 'English':
            data_task_markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("⚡️ At the moment of receiving the task")
            btn2 = types.KeyboardButton("💭 After planning")
            btn3 = types.KeyboardButton("🧘‍♂️ As the need arises")
            data_task_markup1.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id,
                             "How do you typically estimate task completion time?",
                             reply_markup=data_task_markup1)
        elif lang == 'Russian':
            data_task_markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("⚡️ В момент получения задачи")
            btn2 = types.KeyboardButton("💭 После планирования")
            btn3 = types.KeyboardButton("🧘‍♂️ По мере возникновения необходимости")
            data_task_markup1.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id,
                             "Как вы обычно определяете время начала выполнения задачи?",
                             reply_markup=data_task_markup1)

    def question_three_hard(self, message, lang):
        if lang == 'English':
            data_task_markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("⚡️ At the moment of receiving the task")
            btn2 = types.KeyboardButton("💭 After planning")
            btn3 = types.KeyboardButton("🧘‍♂️ As the need arises")
            data_task_markup1.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id,
                             "How do you typically estimate completion time of your hardest task?",
                             reply_markup=data_task_markup1)
        elif lang == 'Russian':
            data_task_markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("⚡️ В момент получения задачи")
            btn2 = types.KeyboardButton("💭 После планирования")
            btn3 = types.KeyboardButton("🧘‍♂️ По мере возникновения необходимости")
            data_task_markup1.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id,
                             "Как вы обычно определяете время начала выполнения вашей самой сложной задачи?",
                             reply_markup=data_task_markup1)

    def question_four(self, message, lang):
        if lang == 'English':
            bot.send_message(message.from_user.id,
                             "Approximately, how many hours do you usually spend on solving a task?\n\nPlease write a "
                             "number")
        elif lang == 'Russian':
            bot.send_message(message.from_user.id,
                             "Примерно сколько часов вы обычно тратите на решение задачи?\nЗапишите числом")

    def question_four_hard(self, message, lang):
        if lang == 'English':
            bot.send_message(message.from_user.id,
                             "Approximately, how many hours do you usually spend on solving a hard task?\n\n Write a "
                             "number")
        elif lang == 'Russian':
            bot.send_message(message.from_user.id,
                             "Примерно сколько часов вы обычно тратите на решение сложной задачи?\nЗапишите числом")

    def question_five(self, message, lang):
        if lang == 'English':
            bot.send_message(message.from_user.id,
                             "Rate how well the task was completed on time from 0 to 10 (where 0 - not completed on "
                             "time,"
                             "10 - completed right on time).\n\n"
                             "Please enter a number from 0 to 10.")
        elif lang == 'Russian':
            bot.send_message(message.from_user.id,
                             "Оцените, насколько ваша задача была бы выполнена в срок от 0 до 10 (где 0 - не "
                             "выполнена в"
                             "срок,"
                             "10 - выполнена точно в срок).\n\n"
                             "Пожалуйста, введите число от 0 до 10.")

    def question_five_hard(self, message, lang):
        if lang == 'English':
            bot.send_message(message.from_user.id,
                             "Rate how well the hardest task was completed on time from 0 to 10 (where 0 - not "
                             "completed on"
                             "time,"
                             "10 - completed right on time).\n\n"
                             "Please enter a number from 0 to 10.")
        elif lang == 'Russian':
            bot.send_message(message.from_user.id,
                             "Оцените, насколько самая сложная задача была бы выполнена вами в срок от 0 до 10 (где 0 -"
                             "не выполнена в срок,"
                             "10 - выполнена точно в срок).\n\n"
                             "Пожалуйста, введите число от 0 до 10.")

    def question_six(self, message, lang):
        if lang == 'English':
            help_data_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Yes")
            btn2 = types.KeyboardButton("No")
            help_data_markup.add(btn1, btn2)
            bot.send_message(message.from_user.id, "Do you receive help from others when completing tasks? (Yes/No)",
                             reply_markup=help_data_markup)
        elif lang == 'Russian':
            help_data_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Да")
            btn2 = types.KeyboardButton("Нет")
            help_data_markup.add(btn1, btn2)
            bot.send_message(message.from_user.id,
                             "Пользуетесь ли вы помощью других лиц при выполнении задач? (Да/Нет)",
                             reply_markup=help_data_markup)

    def question_six_hard(self, message, lang):
        if lang == 'English':
            help_data_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Yes")
            btn2 = types.KeyboardButton("No")
            help_data_markup.add(btn1, btn2)
            bot.send_message(message.from_user.id, "Do you receive help from others when completing the hardest task? "
                                                   "(Yes/No)",
                             reply_markup=help_data_markup)
        elif lang == 'Russian':
            help_data_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Да")
            btn2 = types.KeyboardButton("Нет")
            help_data_markup.add(btn1, btn2)
            bot.send_message(message.from_user.id, "Пользуетесь ли вы помощью других лиц при выполнении самой сложной "
                                                   "задачи? (Да/Нет)",
                             reply_markup=help_data_markup)

    def question_seven(self, message, lang):
        if lang == 'English':
            markup = types.ReplyKeyboardMarkup(row_width=1)
            btn1 = types.KeyboardButton("🟢 High")
            btn2 = types.KeyboardButton("🟡 Medium")
            btn3 = types.KeyboardButton("🔴 Low")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id, "Indicate the priority of your typical task", reply_markup=markup)
        elif lang == 'Russian':
            markup = types.ReplyKeyboardMarkup(row_width=1)
            btn1 = types.KeyboardButton("🟢 Высокий")
            btn2 = types.KeyboardButton("🟡 Средний")
            btn3 = types.KeyboardButton("🔴 Низкий")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id,
                             "Укажите приоритет вашей обычной задачи.", reply_markup=markup)

    def question_seven_hard(self, message, lang):
        if lang == 'English':
            markup = types.ReplyKeyboardMarkup(row_width=1)
            btn1 = types.KeyboardButton("🟢 High")
            btn2 = types.KeyboardButton("🟡 Medium")
            btn3 = types.KeyboardButton("🔴 Low")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id, "Indicate the priority of your hardest task", reply_markup=markup)
        elif lang == 'Russian':
            markup = types.ReplyKeyboardMarkup(row_width=1)
            btn1 = types.KeyboardButton("🟢 Высокий")
            btn2 = types.KeyboardButton("🟡 Средний")
            btn3 = types.KeyboardButton("🔴 Низкий")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id,
                             "Укажите приоритет вашей самой сложной задачи.", reply_markup=markup)

    @bot.message_handler(commands=['survey'])
    def start_survey(self, message, lang):
        self.question_one(message, lang)
