import sqlite3
from datetime import datetime

# Подключение к базе данных
db = sqlite3.connect("mydb.db")

# Функция добавления задачи
def addTask(userId, content):
    # Проверка запроса пользователя на корректность
    errorMessage = messageCheck(1, content)
    # Если запрос составлен некорректно, то функция возвращает
    # сообщение об ошибке
    if errorMessage is not None:
        return errorMessage

    # Дата задачи
    taskDate = content[0].split('.')

    # Если дата введена некорректно, то функция возвращает
    # сообщение об ошибке
    errorMessage = messageCheck(3, taskDate)
    if errorMessage is not None:
        return errorMessage

    # День выполнения задания
    taskDay = int(taskDate[0])
    # Месяц выполнения задания
    taskMonth = int(taskDate[1])
    # Время выполнения задания
    taskTime = content[1]
    # Содержание задания
    taskText = ""

    for i in range(2,len(content)):
        taskText += content[i] + " "

    # Массив с информацией о задаче, которая будет отправлена в БД
    data = (userId, taskDay, taskMonth, taskTime, taskText)

    # Создаем курсор, специальный объект, который делает запросы 
    # и получает их результаты
    dbCursor = db.cursor()
    # Добавляем данные в БД
    dbCursor.execute("INSERT INTO Tasks(UserId, TaskDay, TaskMonth,\
     TaskTime, TaskText) VALUES(?, ?, ?, ?, ?)", data)
    # Сохраняем транзакцию
    db.commit()
    # Закрываем соединение с БД
    dbCursor.close()

    # Возвращаем сообщение, подтверждающее успешное выполнение
    # запроса
    return 'Задание успешно добавлено!'

# Функция, возвращающая список всего расписания
# Принимает на вход идентификатор пользователя
def getAllTasks(userId):
    dbCursor = db.cursor()
    # Выбираем из БД все задания, которые существуют у пользователя
    # с данным идентификатором, и сортируем их по дате
    dbCursor.execute("SELECT * from Tasks WHERE UserId = '%s' \
    ORDER BY TaskMonth, TaskDay, TaskTime" % userId)
    # Список с задачами
    tasksList = dbCursor.fetchall()
    db.commit()
    dbCursor.close()

    # Содержание ответного сообщения
    response = ''

    # Если расписание отсутствует, то возвращаем соответствующее
    # сообщение
    if not tasksList:
        response = 'У Вас нет расписания'

        return response

    # Иначе формируем сообщение с расписанием пользователя
    response  = 'Ваше расписание:\n'

    # Распределяем расписание по дням и формируем структурированное сообщение
    for i in range(0, len(tasksList)):
        if i == 0:
            response += '```spoiler ' + dateForm(tasksList[i][2], \
            tasksList[i][3]) + '\n' + tasksList[i][4] + ' - ' + \
             tasksList[i][5] + '\n'
        elif tasksList[i-1][2] == tasksList[i][2] and \
             tasksList[i-1][3] == tasksList[i][3]:
            response += tasksList[i][4] + ' - ' + tasksList[i][5] + '\n'
        elif tasksList[i-1][2] != tasksList[i][2] \
        or tasksList[i-1][3] != tasksList[i][3]:
            response += '```\n' + '```spoiler ' + \
            dateForm(tasksList[i][2], tasksList[i][3]) + \
            '\n' + tasksList[i][4] + ' - ' + tasksList[i][5] + '\n'
        elif i == len(tasksList) - 1:
            if tasksList[i-1][2] == tasksList[i][2] and \
            tasksList[i-1][3] == tasksList[i][3]:
                response += tasksList[i][4] + ' - ' + \
                tasksList[i][5] + '\n' + '```\n'
            elif tasksList[i-1][2] != tasksList[i][2] or \
            tasksList[i-1][3] != tasksList[i][3]:
                response += '```\n' + '```spoiler ' + \
                dateForm(tasksList[i][2], tasksList[i][3]) + '\n' \
                + tasksList[i][4] + ' - ' + tasksList[i][5] + '\n' + '```\n'

    # Возвращаем переменную с содержанием ответного сообщения
    return response

# Функция, возвращающая сообщение, содержащие расписание
# на конкретный день
# Принимает в качестве аргументов идентификатор пользователя 
# и дату, на которую следует предоставить расписание
def getTasksByDate(userId, content):
    # Дата расписания
    taskDate = content.split('.')

    # Проверка даты на корректность ввода
    errorMessge = messageCheck(3, taskDate)
    if errorMessge is not None:
        return errorMessge

    # День расписания
    taskDay = int(taskDate[0])
    # Месяц расписания
    taskMonth = int(taskDate[1])

    dbCursor = db.cursor()
    # выбираем из БД задачи конкретного пользователя
    # на указанную дату, отсортированные по времени
    dbCursor.execute("SELECT * from Tasks WHERE TaskDay=:taskDay \
    and TaskMonth=:taskMonth and UserId=:userId ORDER BY TaskTime", 
                    {"taskDay": taskDay, "taskMonth": taskMonth, \
                    "userId": userId})
    # Перемнная, содержащая в себе массив с задачами пользователя
    tasksList = dbCursor.fetchall()
    db.commit()
    dbCursor.close()

    # ответное сообщение
    response = ''

    # Если расписания нет, то отправляем соответствующее сообщение
    if not tasksList:
        response  += 'Нет расписания на ' + date
    # Иначе формируем ответ с расписанием на указанную дату
    else:
        response += 'Расписание на ' + date + ':\n'
        for task in tasksList:
            response += task[4] + ' - ' + task[5] + '\n'

    return response

# Функция возвращает расписание на текущий день
# Принимает на вход идентификатор пользователя
def getTodayTasks(userId):
    # Текущий день
    day = datetime.now().day
    # Текущий месяц
    month = datetime.now().month

    dbCursor = db.cursor()
    # Выбираем из БД задачи на текущий день для указанного пользователя
    dbCursor.execute("SELECT * from Tasks WHERE TaskDay=:taskDay \
    and TaskMonth=:taskMonth and UserId=:userId ORDER BY TaskTime", 
                    {"taskDay": day, "taskMonth": month, "userId": userId})
    # Массив со списком задач
    tasksList = dbCursor.fetchall()
    db.commit()
    dbCursor.close()

    # Формируем содержание ответного сообщения
    response = ''

    if not tasksList:
        response  += 'Нет расписания на сегодня, ' + dateForm(day, month)
    else:
        response += 'Расписание на сегодня, ' + dateForm(day, month) + ':\n'
        for task in tasksList:
            response += task[4] + ' - ' + task[5] + '\n'

    return response

# Функция удаляет просроченные задачи
def deleteOldTasks():
    day = datetime.now().day
    month = datetime.now().month

    dbCursor = db.cursor()
    # Удаляет задачи прошедших месяцев
    dbCursor.execute("DELETE from Tasks WHERE TaskMonth<:month",
                    {"month": month})
    # Удаляет задачи текущего месяца прошедших дней
    dbCursor.execute("DELETE from Tasks WHERE \
        TaskMonth=:month and TaskDay<:day",
                    {"month": month, "day": day})
    db.commit()
    dbCursor.close()

# Проверка запроса пользователя на корректность 
# введенных данных
def messageCheck(flag, content):
    if flag == 1:
        if len(content) == 0:
            message = "Введите дату, время и содержание задания"
        elif len(content) == 1:
            message = "Введите время и содержание задания"
        elif len(content) == 2:
            message = "Введите содержание задания"
        else:
            message = None
    elif flag == 3:
        try:
            if len(content) != 2:
                message = "Введите корректную дату. Например, '01.01'"
            elif int(content[0]) > 31:
                message = "Введите корректный день"
            elif int(content[1]) > 12:
                message = "Введите корректный месяц"
            else:
                message = None
        except Exception:
            message = 'Данные введены некорректно'

    return message

# Фуекция преобразовывает дату в формат "ДД.ММ"
def dateForm(day, month):
    date = ''
    
    if day < 9:
        date += '0' + str(day)
    else:
        date += str(day)
    
    date += '.'

    if month < 9:
        date += '0' + str(month)
    else:
        date += str(month)

    return date


'''dbCursor = db.cursor()
dbCursor.execute("DELETE from User")
db.commit()
dbCursor.close()'''