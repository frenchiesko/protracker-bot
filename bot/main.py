import telebot
from telebot import types

import os
from dotenv import load_dotenv

from model import Preprocessor, DataGenerator, Model
from survey import SurveyClass
from task_survey import TaskSurvey
from task_manager import TaskManager


load_dotenv('.env')
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)


from_task = None  # Indicator if question came from survey or after creating new task
current_language = None  # Language interface
task_answers = None  # User's answers after creating task

data = None  # Object for preprocessing survey answers
ml = None # Model
result = None  # Model's prediction
weights = None  # Weights from model


# BOT FUNCTION - Start function with language choosing
@bot.message_handler(commands=['start'])
def start(message):
    global current_language
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton("🇷🇺 Russian")
    btn2 = types.KeyboardButton("🇬🇧 English")
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, "Choose the language", reply_markup=markup)


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


# BOT FUNCTION - bot info
@bot.message_handler(commands=['info'])
def info(message):
    global current_language
    if current_language == 'Russian':
        bot.send_message(message.from_user.id,
                         "ProTracker обеспечивает эффективное управление задачами и аналитику. Используя машинное "
                         "обучение, "
                         "этот бот применяет линейную регрессию для прогнозирования длительности задач.\n\nОбратите "
                         "внимание, "
                         "что как MVP - этот проект может содержать баги и будет совершенствоваться. "
                         "Присоединяйтесь к "
                         "ProTracker для оптимизации управления задачами и получения информативной аналитики!\n\n🌐 "
                         "GitHub: "
                         "https://github.com/frenchiesko/protracker-bot",
                         reply_markup=create_markup(current_language))

    elif current_language == 'English':
        bot.send_message(message.from_user.id,
                         "ProTracker enables effective task management and analytics. Leveraging machine learning, "
                         "this bot employs linear regression to predict task durations.\nPlease note, as an MVP, "
                         "this project may have bugs and will be improving. \nJoin ProTracker to streamline "
                         "your task management and gain insightful analytics!\n\n🌐 GitHub: https://github.com/frenchiesko/protracker-bot",
                         reply_markup=create_markup(current_language))


# FUNCTION - add answers to dict for saving in storage
def process_survey_answer(message, dct, question_number, answer):
    if question_number not in dct:
        dct[question_number] = str(answer)


# FUNCTION - answer data processing
def send_messages(message, lst, dct, index):
    global current_language, from_task, ml, result, weights, data
    if index < len(lst):
        lst[index](message, current_language)
        bot.register_next_step_handler(message, lambda msg: process_survey_answer(message, dct, index, msg.text))
        index += 1
        bot.register_next_step_handler(message, lambda msg: send_messages(msg, lst, dct, index))
    else:

        # If survey data
        if not from_task:
            data = Preprocessor(dct).preprocess_survey_data(message, current_language)
            if data is not None:
                weights = DataGenerator(data).get_weights()
                if weights is not None:
                    # If all answer types are correct
                    if current_language == 'English':
                        bot.send_message(message.from_user.id, "📬 Information successfully sent! Ready for "
                                                               "predictions! Click on /new_task to create a new task")
                    elif current_language == 'Russian':
                        bot.send_message(message.from_user.id, "📬 Информация успешно доставлена! Готово к "
                                                               "предсказаниям! Нажмите на /new_task, чтобы создать "
                                                               "новую задачу")
                    # Model training
                    new_data = weights.generate_data()
                    ml = Model(new_data).training()
                else:
                    if current_language == 'English':
                        bot.send_message(message.from_user.id,
                                         "🚫 Wrong answers format. Take a /survey again")
                    elif current_language == 'Russian':
                        bot.send_message(message.from_user.id,
                                         "🚫 Неверный формат данных. Пройдите опрос снова - /survey")
            else:
                if current_language == 'English':
                    bot.send_message(message.from_user.id,
                                     "🚫 Wrong answers format. Take a /survey again")
                elif current_language == 'Russian':
                    bot.send_message(message.from_user.id,
                                     "🚫 Неверный формат данных. Пройдите опрос снова - /survey")

        # If task data
        else:
            if weights is not None:
                data = Preprocessor(dct).preprocess_task_data(message, current_language)
                if data is not None:
                    if current_language == 'English':
                        bot.send_message(message.from_user.id,
                                         "✅ Task successfully saved!")
                    else:
                        bot.send_message(message.from_user.id,
                                         "✅ Задача успешно сохранена в ваш список!")
                    # ML model's prediction
                    result = Model(data).make_prediction(ml)
                    tm.add_prediction(result)
                else:
                    # If answers format is incorrect
                    if current_language == 'English':
                        bot.send_message(message.from_user.id,
                                         "🚫 Wrong answers format. Try to create /new_task again")
                    elif current_language == 'Russian':
                        bot.send_message(message.from_user.id,
                                         "🚫 Неверный формат данных. Попробуйте создать задачу снова\n/new_task")
            else:
                # If user creates task before taking a survey (for the 1st time)
                if current_language == 'English':
                    bot.send_message(message.from_user.id,
                                     "✅ Task successfully saved! Prediction is not available, I'd recommend you to "
                                     "/delete_task")
                    bot.send_message(message.from_user.id,
                                     "🙁 It seems I don't have survey data. Please retake the /survey. "
                                     "Without it, I won't be able to make predictions")
                elif current_language == 'Russian':
                    bot.send_message(message.from_user.id,
                                     "✅ Задача успешно сохранена в ваш список! Предсказание недоступно. Рекомендую "
                                     "удалить данную задачу через /delete_task")
                    bot.send_message(message.from_user.id,
                                     "🙁 Похоже, у меня нет данных опроса. Пройдите опрос заново. Без него "
                                     "мне не удастся вычислить предсказания.\n/survey")


# Objects
tm = TaskManager()
sc = SurveyClass()
ts = TaskSurvey()

# Survey questions list from SurveyClass
sc_list = [sc.start_survey, sc.question_one_hard, sc.question_two,
           sc.question_two_hard, sc.question_three, sc.question_three_hard,
           sc.question_four, sc.question_four_hard, sc.question_five,
           sc.question_five_hard, sc.question_six, sc.question_six_hard,
           sc.question_seven, sc.question_seven_hard]

# New task questions list from TaskSurvey
at_list = [ts.start_new_task, ts.question_two, ts.question_three, ts.question_four,
           ts.question_five, ts.question_six, ts.question_seven, ts.question_eight]


# BOT FUNCTION - Start a survey
@bot.message_handler(commands=['survey'])
def survey(message):
    global from_task
    new_user_answers = {}
    from_task = False
    send_messages(message, sc_list, new_user_answers, 0)


# BOT FUNCTION - Create new task
@bot.message_handler(commands=['new_task'])
def new_task(message):
    global current_language, from_task
    new_user_answers = {}
    if current_language == 'Russian':
        bot.send_message(message.from_user.id,
                         "👍 Отлично! Чтобы записать вашу задачу в хранилище, пожалуйста, ответьте на несколько "
                         "вопросов."
                         "Это поможет максимально ясно описать задачу, особенно для прогнозирования времени, "
                         "необходимого для "
                         "выполнения. Пожалуйста, отвечайте честно и в том виде, в котором вас просят.\n\n"
                         "🎯 Обратите внимание, что некорректные ответы могут оказать негативное влияние на "
                         "предсказания.",
                         reply_markup=create_markup(current_language))

        from_task = True
        send_messages(message, at_list, new_user_answers, 0)
        tm.create_task(new_user_answers)
        task_answers = new_user_answers
    elif current_language == 'English':
        bot.send_message(message.from_user.id,
                         "👍 Great! To store your task, please answer a few questions. This will help provide a clear "
                         "description, "
                         "especially for predicting the time needed to complete it. Please answer truthfully and as "
                         "requested.\n\n"
                         "🎯 Note that inaccurate responses may adversely affect model's predictions.",
                         reply_markup=create_markup(current_language))

        from_task = True
        send_messages(message, at_list, new_user_answers, 0)
        tm.create_task(new_user_answers)
        task_answers = new_user_answers


# BOT FUNCTION - Show user's task list
@bot.message_handler(commands=['my_tasks'])
def my_tasks(message):
    global current_language
    tm.show_tasks(message, current_language)


# BOT FUNCTION - task info
@bot.message_handler(commands=['task_info'])
def task_info(message):
    global current_language
    if current_language == 'English':
        bot.send_message(message.from_user.id, "Enter task number")
    elif current_language == 'Russian':
        bot.send_message(message.from_user.id, "Введите номер задачи")
    bot.register_next_step_handler(message, process_task_info_request)


# FUNCTION - get information about task
def process_task_info_request(message):
    global current_language
    number = message.text.strip()
    get_info = tm.get_task_info(message, int(number), current_language)
    if not isinstance(get_info, bool) and get_info is not None:
        if current_language == 'English':
            inf = (f"📌 Task: {get_info['title']}\n\n"
                   f"📄 Description:\n{get_info['description']}\n\n"
                   f"🔗 Materials and resources:\n{get_info['resources']}\n\n"
                   f"🏅 Task priority: {get_info['priority']}\n"
                   f"📈 Difficulty level: {get_info['diff_level']}\n"
                   f"Start date: {get_info['start']}\n"
                   f"⏱ Time needed: ~{get_info['prediction']} hrs")
        elif current_language == 'Russian':
            inf = (f"📌 Задача: {get_info['title']}\n\n"
                   f"📄 Описание:\n{get_info['description']}\n\n"
                   f"🔗 Материалы и ресурсы:\n{get_info['resources']}\n\n"
                   f"🏅 Приоритет задачи: {get_info['priority']}\n"
                   f"📈 Уровень сложности: {get_info['diff_level']}\n\n"
                   f"📆 Дата начала: {get_info['start']}\n"
                   f"⏱ Часов потребуется на выполнение: ~{get_info['prediction']}")

        if task_info:
            bot.send_message(message.from_user.id, inf)
        else:
            if current_language == 'English':
                bot.send_message(message.from_user.id,
                                 "✖️ No task with this number was found. Please enter the correct task number")
            elif current_language == 'Russian':
                bot.send_message(message.from_user.id,
                                 "✖️ Задачи с таким номером не найдено. Пожалуйста, введите правильный номер задачи.")
    else:
        if current_language == 'English':
            bot.send_message(message.from_user.id,
                             "✖️ No task with this number was found. Please enter the correct task number")
        elif current_language == 'Russian':
            bot.send_message(message.from_user.id,
                             "✖️ Задачи с таким номером не найдено. Пожалуйста, введите правильный номер задачи.")



# FUNCTION - perform deleting task
def process_delete_task(message):
    global current_language
    number = message.text.strip()
    if current_language == 'English':
        dl = tm.delete_task(message, number, current_language)
        if isinstance(dl, bool):
            bot.send_message(message.from_user.id, "Task successfully deleted!")
    elif current_language == 'Russian':
        dl = tm.delete_task(message, number, current_language)
        if isinstance(dl, bool):
            bot.send_message(message.from_user.id, "Задача успешно удалена!")


# BOT FUNCTION - Delete task from storage
@bot.message_handler(commands=['delete_task'])
def delete_task(message):
    global current_language
    if current_language == 'English':
        bot.send_message(message.from_user.id, "Enter task number (1-10)")
    elif current_language == 'Russian':
        bot.send_message(message.from_user.id, "Введите номер задачи (1-10)")
    bot.register_next_step_handler(message, process_delete_task)


# BOT FUNCTION - show descriptive statisics about tasks
@bot.message_handler(commands=['analytics'])
def analytics(message):
    global current_language
    tm.task_data(message, current_language)


# BOT FUNCTION - Text message handler
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global current_language, user_answers
    user_id = message.from_user.id

    if message.text == '🇷🇺 Russian':
        current_language = 'Russian'
        markup = create_markup(current_language)
        bot.send_message(message.from_user.id,
                         "👋 Привет! Для начала, рекомендую пройти опрос. Это позволит мне понять "
                         "твои предыдущие паттерны работы и сделать предсказания "
                         "по твоим задачам."
                         "\nПросто используй команду /survey, чтобы начать опрос.\n\n 🎯 Обрати "
                         "внимание, что некорректные ответы могут оказать негативное влияние на "
                         "машинное обучение.\n"
                         "Если нужна помощь - я всегда здесь!", reply_markup=markup)
    elif message.text == '🇬🇧 English':
        current_language = 'English'
        markup = create_markup(current_language)
        bot.send_message(message.from_user.id,
                         "👋 Hi! To start off, I recommend taking a survey. It'll help me understand your previous "
                         "work patterns and make accurate predictions for your tasks."
                         "\nJust use the command /survey to begin the survey.\n\n 🎯 Please note that incorrect answers "
                         "may"
                         "have a negative impact on the machine learning"
                         "model's predictions.\nI'm here to assist if you need any help!",
                         reply_markup=markup)


    # Buttons interaction
    elif message.text == '❓ Пройти опрос' or message.text == '❓ Take a survey':
        survey(message)
    elif message.text == '👀 О боте' or message.text == '👀 About bot':
        info(message)
    elif message.text == '🆕 Новая задача' or message.text == '🆕 New task':
        new_task(message)
    elif message.text == '📄 Мои задачи' or message.text == '📄 My tasks':
        my_tasks(message)
    elif message.text == '❌ Удалить задачу' or message.text == '❌ Delete task':
        delete_task(message)
    elif message.text == '📊 Аналитика' or message.text == '📊 Analytics':
        analytics(message)
    elif message.text == '📖Рассмотреть задачу' or message.text == '📖 Task info':
        task_info(message)
    else:
        handle_unknown_message(message)


# BOT FUNCTION - for unknown text
@bot.message_handler(func=lambda message: True)
def handle_unknown_message(message):
    global current_language
    response = {
        'English': "I'm sorry, I didn't understand that. Here are the available commands:\n"
                   "❓ /survey - start a survey\n"
                   "👀 /info - learn about the bot\n"
                   "🆕 /new_task - create a new task\n"
                   "📄 /my_tasks - view my tasks\n"
                   "❌ /delete_task - delete a task\n"
                   "📊 /analytics - view analytics\n"
                   "📖 /task_info - view task information",
        'Russian': "Извините, я не понял ваш запрос. Вот список доступных команд:\n"
                   "❓ /survey - начать опрос\n"
                   "👀 /info - узнать о боте\n"
                   "🆕 /new_task - создать новую задачу\n"
                   "📄 /my_tasks - просмотреть мои задачи\n"
                   "❌ /delete_task - удалить задачу\n"
                   "📊 /analytics - просмотреть аналитику\n"
                   "📖 /task_info - просмотреть информацию о задаче"
    }
    bot.reply_to(message, response[current_language])


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
