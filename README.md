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


## Bot files


`main.py` - The main file of the bot, user message input and processing

`survey.py` - The file responsible for conducting the initial survey to gather coefficients for model, to be later used in preprocessing and generating the training dataset within `model.py`

`task_survey.py` - The file responsible for collecting data when creating a new task for subsequent analysis and predictions from `model.py`

`task_manager.py` - The file implementing storage, addition, deletion of tasks, displaying task information, and presenting visual analytics

`model.py` - The file where data preprocessing of surveys and tasks occurs, including coefficient computation, data generation, model training, and prediction execution


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


## License

[MIT](https://choosealicense.com/licenses/mit/)
