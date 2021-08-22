import sqlite3
import re
from datetime import datetime


db = sqlite3.connect("mydb.db")


def checkUser(userId):
    dbCursor = db.cursor()
    dbCursor.execute("SELECT * from User WHERE UserId = '%s'" % userId)
    userInfo = dbCursor.fetchall()
    db.commit()
    dbCursor.close()

    if not userInfo:
        return 0
    else:
        return 1


def helloMessage():
    message = "Добро пожаловать!\n"
    message += "Меня зовут Просто Бот\n"
    message += "Так как Вы впервые пользуетесь мной, я прошу Вас немного рассказать о себе.\n"
    message += "Пожалуйста, введите попорядку через пробел свои ФИО, дату рождения, пол и номер телефона.\n"
    message += "Перед личной информацией введите 'Добавить информацию'.\n"
    message += "Например, 'Добавить информацию Иванов Иван Иванович 12.12.1991 м +79991234567'"

    return message


def getUserInfo(userId, content):
    lastName = ''
    firstName = ''
    middleName = ''
    gender = ''
    phone = ''

    if len(content) != 6:
        message = "Пожалуйста, введите запрос корректно.\n"
        message += "Если Вы хотите добавить информацию о себе, то введите, например, 'добавить информацию Иванов Иван Иванович 12.12.1991 м +79991234567'"

        return message
    elif len(content[3].split('.')) != 3:
        message = "Пожалуйста, введите дату рождения корректно.\n"
        message += "Например, '12.12.1991'"

        return message
    else:
        lastName = capitalizeTheFirstLetter(content[0])
        firstName = capitalizeTheFirstLetter(content[1])
        middleName = capitalizeTheFirstLetter(content[2])
        gender = content[4]
        phone = content[5]
        day = content[3].split('.')[0]
        month = content[3].split('.')[1]
        year = content[3].split('.')[2]

    if not checkGender(gender):
        message = "Пожалуйста, введите Ваш пол корректно. Например, 'ж'"

        return message

    if not checkPhone(phone):
        message = "Пожалуйста, введите Ваш номер телефона корректно. Например, '+79991234567'"

        return message

    if not checkDay(day):
        message = 'Вы ввели дату дня рождения неккоректно'
        print(checkDay(day))

        return message

    if not checkMonth(month):
        message = 'Вы ввели дату дня рождения неккоректно'
        print("месяц", checkMonth(month))
        return message

    if not checkYear(year):
        message = 'Вы ввели дату дня рождения неккоректно'
        print('год', checkYear(year))

        return message

    if gender == 'м':
        dbGender = 'male'
    elif gender == 'ж':
        dbGender = 'female'

    data = (userId, lastName, firstName, middleName, dbGender, userId, phone, int(day), int(month), int(year))

    dbCursor = db.cursor()
    dbCursor.execute("INSERT INTO User(UserId, Surname, FirstName, MiddleName, Gender, Email, Phone, BirthdayDay, BirthdayMonth, BirthdayYear) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    db.commit()
    dbCursor.close()

    message = '''
    Информация успешно добавлена!

    Напишите мне 'Информация', чтобы узнать о том, какие команды я знаю.
    '''

    return message


def capitalizeTheFirstLetter(word):
    newWord = word[0].upper()
    newWord += word[1:]

    return newWord


def checkGender(gender):
    if len(gender) != 1 or gender[0].lower() != 'м' and gender[0].lower() != 'ж':
        return 0
    else:
        return 1


def checkPhone(phone):
    if re.match(r'[+]{1}[7]{1}[0-9]{10}', phone) and len(phone) == 12:
        return 1
    else:
        return 0


def checkDay(day):
    try:
        if int(day) < 1 or int(day) > 31:
            return 0
    except Exception:
            return 0
    
    return 1


def checkMonth(month):
    try:
        if int(month) < 1 or int(month) > 12:
            return 0
    except Exception:
            return 0
    
    return 1


def checkYear(year):
    try:
        if int(year) < 1800 or int(year) > getCurrentYear():
            return 0
    except Exception:
            return 0
    
    return 1


def getCurrentYear():
    year = datetime.now().year

    return year