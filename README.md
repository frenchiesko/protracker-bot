# ProTracker bot

This bot serves as a simple and intuitive task scheduler, offering brief analytics for your task list. It utilizes linear regression to predict task completion hours at the moment of task creation. To gather user pattern data and work routines, an inquiry is conducted, followed by data preprocessing and necessary model training data generation. The project will continue to be refined and improved.
## Bot commands

`/start` - start the bot

`/survey` - start a survey to collect data about user's work patterns

`/info` - information about bot (brief, URL)

`/new_task` - create new task to task list

`/delete_task` - delete task from task list

`/analytics` - send a few charts about user's tasks categories

`/task_info` - send information about task (date, priority, difficulty, how many hrs need to get task done)

## Demo
![Bot working](demo.gif)


## Installation

1. Clone this repository:

    ```bash
    https://github.com/frenchiesko/protracker-bot.git
    ```

2. Navigate to the project directory:

    ```bash
    cd protracker-bot
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a configuration file `.env` and specify API TOKEN (get it from @BotFather):

    ```
    TOKEN=your_token
    ```

5. Start the bot with command:

    ```bash
    python main.py
    ```
## Bot files


`main.py` - The main file of the bot, user message input and processing

`survey.py` - The file responsible for conducting the initial survey to gather coefficients for model, to be later used in preprocessing and generating the training dataset within `model.py`

`task_survey.py` - The file responsible for collecting data when creating a new task for subsequent analysis and predictions from `model.py`

`task_manager.py` - The file implementing storage, addition, deletion of tasks, displaying task information, and presenting visual analytics

`model.py` - The file where data preprocessing of surveys and tasks occurs, including coefficient computation, data generation, model training, and prediction execution

## Function and classes

The machine learning process in the model involves the following steps:

The answers from `survey.py` are passed to the `Preprocessor` class in `model.py`, where they are processed (formatted, encoded).
The processed data is then passed to the `DataGenerator` class in the `get_weights` function. In this function, the coefficients (`coef_`) and the intercept (`intercept_`) from the trained linear regression model are obtained based on the processed data.
In the same class, the `generate_data` function randomly generates a training dataset with 5 features. After generating the features, the target variable values are calculated using the formula: `y_i = intercept_ + (x_1*coef_1 + ... + x_n*coef_n)`
After generating the data, the linear regression model is trained on the dataset, after preprocessing and encoding the data. The R2-score and MAE metrics are used for model evaluation.
The trained model is then saved and used for making predictions after creating each task, provided that the user enters the data in the correct format.

### ML classes and functions

The following functions and classes are used in the machine learning process:

`Preprocessor` class: This class is responsible for processing the answers from the survey, including formatting and encoding.
`DataGenerator` class: This class generates the training dataset and obtains the coefficients and intercept from the trained linear regression model.
`get_weights` function: This function retrieves the coefficients and intercept from the trained linear regression model.
`generate_data` function: This function generates the training dataset with 5 features and calculates the target variable values.

Model evaluation: The R2-score and MAE metrics are used to evaluate the trained linear regression model.

## Usage

Make sure to run `survey.py` to collect the answers from the survey.
Pass the collected answers to the `Preprocessor` class in model.py to process the data.
Use the processed data as input for the `DataGenerator` class and call the `get_weights` function to obtain the coefficients and intercept from the trained linear regression model.
Call the `generate_data` function in the `DataGenerator` class to generate the training dataset and calculate the target variable values.
Preprocess and encode the generated data before training the linear regression model.
Use the R2-score and MAE metrics to evaluate the trained model.
Save the trained model for future use.
Make predictions using the saved model after creating each task, ensuring that the user enters the data in the correct format.
Please note that the accuracy of the predictions may vary depending on the quality and quantity of the collected survey answers.

## Tech stack

**Machine Learning and Analytics:** pandas, numpy, scikit-learn, matplotlib, seaborn


## License

[MIT](https://choosealicense.com/licenses/mit/)
