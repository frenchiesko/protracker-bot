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
## Tech stack

**Machine Learning and Analytics:** pandas, numpy, scikit-learn, matplotlib, seaborn


## License

[MIT](https://choosealicense.com/licenses/mit/)
