import telebot
from telebot import types

import io
import os
from dotenv import load_dotenv

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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


# TASK CLASS - class for interaction with tasks
class TaskManager:

    def __init__(self):
        self.storage = []
        self.preds = []

    def create_task(self, task):
        self.storage.append(task)

    def add_prediction(self, pred):
        self.preds.append(pred)

    def show_tasks(self, message, lang):
        if lang == 'English':
            if len(self.storage) == 0:
                bot.send_message(message.from_user.id,
                                 "You have no tasks right now. Click /new_task to create new one!")
            else:
                bot.send_message(message.from_user.id,
                                 "📝 Your Task list")
        elif lang == 'Russian':
            if len(self.storage) == 0:
                bot.send_message(message.from_user.id,
                                 "На данный момент у вас нет задач. Нажмите на /new_task, чтобы создать новую!")
            else:
                bot.send_message(message.from_user.id,
                                 "📝 Ваш список задач")
        task_list = ""
        counter = 1
        for task in self.storage:
            task_list += f'{counter}. {task[2]}\n'
            counter += 1
        bot.send_message(message.from_user.id, task_list)

    # FUNCTION - Make graphs about task categories (simple analytics)
    def task_data(self, message, lang):
        if 3 > len(self.storage):
            if lang == 'English':
                bot.send_message(message.from_user.id,
                                 "📊 You need at least three tasks to generate analytics. Surprise me with a longer "
                                 "task list for more precise analysis! 📈"
                                 "\nClick /new_task to create new one.")
                return False
            elif lang == 'Russian':
                bot.send_message(message.from_user.id,
                                 "📊 Для получения аналитических данных необходимо иметь как минимум три задачи. "
                                 "Обрадуйте меня большим списком задач для более точного анализа! 📈!"
                                 "\nНажмите на /new_task, чтобы создать новую задачу.")
                return False
        elif 3 <= len(self.storage):
            if lang == 'English':
                bot.send_message(message.from_user.id, "🔎 Here's your personalized analysis of the graphs!")

                priority = [task[5] for task in self.storage]
                when_start = [task[6] for task in self.storage]
                independent = [task[7] for task in self.storage]
                diff_lvl = [task[8] for task in self.storage]
            elif lang == 'Russian':
                bot.send_message(message.from_user.id, "🔎 Вот ваш персональный анализ графиков!")

                priority = [task[5] for task in self.storage if task[5]]
                when_start = [task[6] for task in self.storage if task[6]]
                independent = [task[7] for task in self.storage if task[7]]
                diff_lvl = [task[8] for task in self.storage if task[8]]

            data = pd.DataFrame({'priority': priority, 'when_start': when_start,
                                 'is_independently': independent, 'difficulty_lvl': diff_lvl})

            data['priority'] = data['priority'].apply(lambda x: x[2:])
            data['when_start'] = data['when_start'].apply(lambda x: x[2:])
            plots = []
            # Check count of categories
            if 1 <= len(data['priority'].unique()) <= 3:
                # Plot 1 - Pie chart for priority
                fig1, ax1 = plt.subplots(figsize=(7, 7))
                priority_cat = list(data["priority"].value_counts().index)
                sizes = list(data["priority"].value_counts())
                ax1.pie(sizes, labels=priority_cat, autopct="%1.1f%%")
                ax1.set_title("Priority" if lang == 'English' else 'Приоритетность задач')
                plots.append(fig1)

            if 1 <= len(data['when_start'].unique()) <= 3:
                # Plot 2 - Pie chart for start time
                fig2, ax2 = plt.subplots(figsize=(7, 7))
                start_cat = list(data["when_start"].value_counts().index)
                sizes = list(data["when_start"].value_counts())
                ax2.pie(sizes, labels=start_cat, autopct="%1.1f%%")
                ax2.set_title("When to Start" if lang == 'English' else 'Когда начинать задачу')
                plots.append(fig2)

            if 1 <= len(data['is_independently'].unique()) <= 2:
                # Plot 3 - Countplot for independence
                fig3, ax3 = plt.subplots(figsize=(7, 5))
                sns.countplot(data=data, x='is_independently', ax=ax3)
                ax3.set_xlabel("Independently" if lang == 'English' else "Самостоятельно")
                ax3.set_title("Independence" if lang == 'English' else 'Самостоятельное выполнение задач')
                plots.append(fig3)

                for plot in plots:
                    # Adding language-dependent supertitle
                    if lang == 'English':
                        plot.suptitle("Task Categories", fontsize=16, y=1.5)
                    elif lang == 'Russian':
                        plot.suptitle("Исследование категорий по задачам", fontsize=16, y=1.5)

                    # Save each plot in a buffer and send separately
                    img_buffer = io.BytesIO()
                    plot.savefig(img_buffer, format='png')
                    img_buffer.seek(0)
                    bot.send_photo(message.from_user.id, photo=img_buffer)

            else:
                if lang == 'English':
                    bot.send_message(message.from_user.id,
                                     "It seems that you tasks format is incorrect. Unfortunately, I can't send you "
                                     "task analytics. /task_info")
                elif lang == 'Russian':
                    bot.send_message(message.from_user.id, "Похоже у вас неправильный формат задач. С ними я не смогу "
                                                           "вывести вам аналитику. /task_info")

    def get_task_info(self, message, number, lang):
        if len(self.storage) == 0:
            if lang == 'English':
                bot.send_message(message.from_user.id, "You have no tasks right now. Click /new_task to create new one")
                return False
            elif lang == 'Russian':
                bot.send_message(message.from_user.id,
                                 "На данный момент у вас нет задач. Нажмите на /new_task, чтобы создать новую!")
                return False

        elif 1 <= number <= len(self.storage):
            task = self.storage[number - 1]
            result = {
                'start': task[1],
                'title': task[2],
                'description': task[3],
                'resources': task[4],
                'priority': task[5],
                'when_to_start': task[6],
                'independently': task[7],
                'diff_level': task[8]
            }
            if len(self.preds) >= number:
                result['prediction'] = self.preds[number - 1]
            else:
                result['prediction'] = '?'
            return result
        else:
            return None

    def delete_task(self, message, number, lang):
        if lang == 'English':
            if len(self.storage) == 0:
                bot.send_message(message.from_user.id, "You have no tasks right now. Click /new_task to create new one")
            else:
                task = self.storage[int(number) - 1]
                self.storage.remove(task)
                return True
        elif lang == 'Russian':
            if len(self.storage) == 0:
                bot.send_message(message.from_user.id,
                                 "На данный момент у вас нет задач. Нажмите на /new_task, чтобы создать новую!")
            else:
                task = self.storage[int(number) - 1]
                self.storage.remove(task)
                return True
