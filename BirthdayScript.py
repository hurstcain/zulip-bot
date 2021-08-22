import zulip
import sqlite3
from datetime import datetime


db = sqlite3.connect("mydb.db")

client = zulip.Client(config_file="/home/pcell/Документы/zulipBot/simpleBot/.zuliprc")


def checkToday():
    todayDate = getTodayDate()

    dbCursor = db.cursor()
    dbCursor.execute("SELECT * from User WHERE BirthdayDay=:day and BirthdayMonth=:month",
                    {"day": todayDate[0], "month": todayDate[1]})
    birthdayPerson = dbCursor.fetchall()
    db.commit()
    dbCursor.close()

    if not birthdayPerson:
        return
    else:
        for person in birthdayPerson:
            sendHappyBirthday(person[0], person[2])
            sendReminder(person[0], person[1], person[2], person[3])


def sendHappyBirthday(id, name):
    content = name + ', с днем рождения!'

    request = {
        "type": "private",
        "to": id,
        "content": content
    }

    client.send_message(request)


def sendReminder(id, surname, firstName, middleName):
    dbCursor = db.cursor()
    dbCursor.execute("SELECT * from User WHERE UserId!=:id",
                    {"id": id})
    users = dbCursor.fetchall()
    db.commit()
    dbCursor.close()
    
    content = surname + ' ' + firstName + ' ' + middleName + ' '
    content += 'отмечает сегодня свой день рождения. \n'
    content += 'Не забудьте отправить поздравления!'

    for user in users:
        request = {
        "type": "private",
        "to": user[0],
        "content": content
        }

        client.send_message(request)


def getTodayDate():
    day = datetime.now().day
    month = datetime.now().month

    return [day, month]


checkToday()