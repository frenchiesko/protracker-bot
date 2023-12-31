# Бот ProTracker

Этот бот служит простым и интуитивно понятным планировщиком задач, предлагая краткую аналитику для вашего списка задач. Он использует линейную регрессию для прогнозирования часов завершения задачи в момент её создания. Для сбора данных о паттернах пользовательского поведения и рабочих рутинах проводится опрос, за которым следует предварительная обработка данных и генерация необходимых данных для обучения модели. Проект будет продолжать совершенствоваться и улучшаться.

## Команды бота

- `/start` - начать бота
- `/survey` - начать опрос для сбора данных о рабочих паттернах пользователя
- `/info` - информация о боте (краткая, URL)
- `/new_task` - создать новую задачу в списке задач
- `/delete_task` - удалить задачу из списка задач
- `/analytics` - отправить несколько графиков о категориях задач пользователя
- `/task_info` - отправить информацию о задаче (дата, приоритет, сложность, сколько часов требуется для выполнения задачи)


## Файлы бота

- `main.py` - Основной файл бота, ввод и обработка сообщений пользователя
- `survey.py` - Файл, отвечающий за проведение начального опроса для сбора коэффициентов для модели, которые затем используются в предобработке и генерации обучающего набора данных в `model.py`
- `task_survey.py` - Файл, отвечающий за сбор данных при создании новой задачи для последующего анализа и прогнозирования из `model.py`
- `task_manager.py` - Файл, реализующий хранение, добавление, удаление задач, отображение информации о задаче и представление визуальной аналитики
- `model.py` - Файл, где происходит предобработка данных из опросов и задач, включая вычисление коэффициентов, генерацию данных, обучение модели и выполнение прогнозов


## Использование

- Убедитесь, что вы запустили `survey.py`, чтобы собрать ответы из опроса.
- Передайте собранные ответы в класс `Preprocessor` в `model.py` для обработки данных.
- Используйте обработанные данные в качестве входных данных для класса `DataGenerator` и вызовите функцию `get_weights`, чтобы получить коэффициенты и перехват из обученной модели линейной регрессии.
- Вызовите функцию `generate_data` в классе `DataGenerator` для создания обучающего набора данных и расчета значений целевой переменной.
- Предварительно обработайте и закодируйте сгенерированные данные перед обучением модели линейной регрессии.
- Используйте метрики R2-score и MAE для оценки обученной модели.
- Сохраните обученную модель для последующего использования.
- Делайте прогнозы с использованием сохраненной модели после создания каждой задачи, обеспечивая правильный формат ввода данных пользователем.

Обратите внимание, что точность прогнозов может варьироваться в зависимости от качества и количества собранных ответов из опроса.

## Лицензия

[MIT](https://choosealicense.com/licenses/mit/)
