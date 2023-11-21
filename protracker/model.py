import telebot

import os
from dotenv import load_dotenv

import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression
# from sklearn.metrics import r2_score, mean_absolute_error

from task_manager import TaskManager


tm = TaskManager()
load_dotenv('.env')
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)


# CLASS - preprocessing data before getting coefficients and model training
class Preprocessor:

    def __init__(self, data):
        self.data = data

    def preprocess_survey_data(self, message, lang):
        # Prepare data
        value_list = []
        for key, value in self.data.items():
            value_list.append(value)

        try:
            survey_data = pd.DataFrame(
                {'difficulty': [round((int(value_list[0]) + int(value_list[2])) / 2),
                                round((int(value_list[1]) + int(value_list[3])) / 2)],
                 'how_fast': [value_list[4], value_list[5]],
                 'hours': [value_list[6], value_list[7]],
                 'deadline_rate': [value_list[8], value_list[9]],
                 'helped': [value_list[10], value_list[11]],
                 'priority': [value_list[12], value_list[13]]})

            # Formatting
            survey_data['hours'] = survey_data['hours'].astype(int)  # -- target
            survey_data['deadline_rate'] = survey_data['deadline_rate'].astype(int)

            # Renaming priority category
            def prior(x):
                if x == '🟢 Высокий' or x == '🟢 High':
                    return 'High'
                elif x == '🟡 Средний' or x == '🟡 Medium':
                    return 'Medium'
                elif x == '🔴 Низкий' or x == '🔴 Low':
                    return 'Low'
            survey_data['priority'] = survey_data['priority'].apply(lambda x: prior(x))

            # Replacing binary with number
            def used(x):
                if x.lower() == 'yes' or x.lower() == 'да':
                    return 1
                elif x.lower() == 'no' or x.lower() == 'нет':
                    return 0
            survey_data['helped'] = survey_data['helped'].apply(lambda x: used(x))

            # Renaming speed category
            def fast(x):
                if x == '🧘\u200d♂️ As the need arises' or x == '🧘\u200d♂️ По мере возникновения необходимости':
                    return 'Slow'
                elif x == '⚡️ At the moment of receiving the task' or x == '⚡️ В момент получения задачи':
                    return 'Fast'
                elif x == '💭 After planning' or x == '💭 После планирования':
                    return 'Moderate'
            survey_data['how_fast'] = survey_data['how_fast'].apply(lambda x: fast(x))

            print(survey_data.head())
            return survey_data

        except ValueError:
            return None

    def preprocess_task_data(self, message, lang):
        # Prepare data
        value_list = []
        for key, value in self.data.items():
            value_list.append(value)
        value_list = value_list[4:]

        # Preprocess data
        task_data = pd.DataFrame({'priority': [value_list[0]], 'how_fast': [value_list[1]],
                                  'helped': [value_list[2]], 'total_difficulty': [value_list[3]]})
        try:
            encoder = LabelEncoder()

            task_data['total_difficulty'] = task_data['total_difficulty'].astype(int)

            # Renaming priority category
            def prior(x):
                if x == '🟢 Высокий' or x == '🟢 High':
                    return 'High'
                elif x == '🟡 Средний' or x == '🟡 Medium':
                    return 'Medium'
                elif x == '🔴 Низкий' or x == '🔴 Low':
                    return 'Low'
            task_data['priority'] = task_data['priority'].apply(lambda x: prior(x))
            encoder.fit(task_data['priority'])
            task_data['priority'] = encoder.transform(task_data['priority'])

            # Renaming speed category
            def fast(x):
                if x == '🤷 Unknown' or x == '🤷 Отложено':
                    return 'Unknown'
                elif x == '⚡️ Today' or x == '⚡️ Сегодня':
                    return 'Today'
                elif x == '💭 During the day' or x == '💭 В течение дня':
                    return 'Day'
            task_data['how_fast'] = task_data['how_fast'].apply(lambda x: fast(x))
            encoder.fit(task_data['how_fast'])
            task_data['how_fast'] = encoder.transform(task_data['how_fast'])

            # Replacing binary with number
            def used(x):
                if x.lower() == 'yes' or x.lower() == 'да':
                    return 1
                elif x.lower() == 'no' or x.lower() == 'нет':
                    return 0
            task_data['helped'] = task_data['helped'].apply(lambda x: used(x))

            print(task_data.head())
            return task_data

        except ValueError:
            return None


# CLASS - get coefficient with Linear Regression to generate train data
class DataGenerator:

    def __init__(self, data):  # data -> survey data
        # weights
        self.coef_ = None
        self.intercept_ = None
        self.data = data

    def get_weights(self):
        y = self.data['hours']
        X = self.data.drop(columns=['hours'])
        # Encoding
        encoder = LabelEncoder()
        X['priority'] = encoder.fit_transform(X['priority'])
        X['how_fast'] = encoder.fit_transform(X['how_fast'])

        try:
            model = LinearRegression()
            model.fit(X, y)
        except ValueError:
            return None

        self.coef_ = model.coef_
        self.intercept_ = model.intercept_
        print(self.coef_)
        print(self.intercept_)

        return self

    def generate_data(self):
        np.random.seed(42)
        num_samples = 600

        categories_speed = ['Slow', 'Moderate', 'Fast']
        categories_priority = ['Low', 'Medium', 'High']

        # Data generation
        train_data = {
            'priority': np.random.choice(categories_priority, size=num_samples),
            'how_fast': np.random.choice(categories_speed, size=num_samples),
            'helped': np.random.randint(0, 1, size=num_samples),
            'total_difficulty': np.random.randint(0, 10, size=num_samples)
        }
        train_data = pd.DataFrame(train_data)

        # Encoding categorial features for target calc
        encoder = LabelEncoder()
        train_data['priority'] = encoder.fit_transform(train_data['priority'])
        train_data['how_fast'] = encoder.fit_transform(train_data['how_fast'])

        if self.coef_ is None or self.intercept_ is None:
            print("Please run 'get_weights' method first.")
            return None

        # Calculate days based on the trained model using linear equation
        train_data['hours'] = abs(round(self.intercept_))
        train_data['hours'] += abs(round(self.coef_[0] * train_data['priority']))
        train_data['hours'] += abs(round(self.coef_[1] * train_data['how_fast']))
        train_data['hours'] += abs(round(self.coef_[2] * train_data['helped']))
        train_data['hours'] += abs(round(self.coef_[3] * train_data['total_difficulty']))

        train_data['hours'] = train_data['hours'].astype(int)

        return train_data


class Model:

    def __init__(self, train_data=None):
        self.train_data = train_data

    def training(self):
        y = self.train_data['hours'].values
        X = self.train_data.drop(columns=['hours'])

        # Data Normalization
        scaler = MinMaxScaler()
        scaler.fit(X)
        X = scaler.transform(X)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25
        )

        lr = LinearRegression()
        lr.fit(X_train, y_train)
        y_pred = lr.predict(X_test)

        # Check metrics and model accuracy
        # print(f"Linear Regrression\nr2 = {r2_score(y_pred, y_test)}\nMAE = {mean_absolute_error(y_pred, y_test)}\n")

        # Returning model to make task prediction
        return lr

    def make_prediction(self, model):
        try:
            # Test normalization
            scaler = MinMaxScaler()
            scaler.fit(self.train_data)
            prediction = model.predict(scaler.transform(self.train_data))
            time = round(abs(float(prediction)))
            return time
        except ValueError:
            return '?'

