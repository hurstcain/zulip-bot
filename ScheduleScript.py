import zulip
import sqlite3
from datetime import datetime
import Schedule


db = sqlite3.connect("mydb.db")

client = zulip.Client(config_file="/home/pcell/Документы/zulipBot/simpleBot/.zuliprc")


def checkToday():
    todayDate = getTodayDate()

    dbCursor = db.cursor()
    dbCursor.execute("SELECT * from Tasks WHERE TaskDay=:day and TaskMonth=:month",
                    {"day": todayDate[0], "month": todayDate[1]})
    todayTasks = dbCursor.fetchall()
    db.commit()
    dbCursor.close()

    if not todayTasks:
        return
    else:
        users = []

        for task in todayTasks:
            if task[1] not in users:
                users.append(task[1])
        
        for user in users:
            content = Schedule.getTodayTasks(user)

            request = {
                "type": "private",
                "to": user,
                "content": content
            }

            client.send_message(request)


def getTodayDate():
    day = datetime.now().day
    month = datetime.now().month

    return [day, month]


checkToday()