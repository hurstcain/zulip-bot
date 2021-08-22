import zulip
import Schedule
import Users
import UserInfo
import Docs
import BotInfo
import Holydays

client = zulip.Client(config_file="/home/pcell/Документы/zulipBot/simpleBot/.zuliprc")

BOT_MAIL = "simpleBot-bot@zulipchat.com"


def checkMsgOnDocsName(content):
    docs = Docs.getDocsList()

    for doc in docs:
        if str(doc[0]) in content or doc[1].lower() in content:
            return True

    return False


def send_msg(msg, content):
    if msg["type"] == 'private':
        request = {
            "type": "private",
            "to": msg["sender_email"],
            "content": content
        }

        client.send_message(request)
    elif msg["type"] == 'stream':
        request = {
            "type": "stream",
            "to": msg["display_recipient"],
            "topic": msg["subject"],
            "content": content
        }

        client.send_message(request)


def send_file(msg, pathToFile):
    with open(pathToFile, "rb") as fp:
        result = client.upload_file(fp)

    if msg["type"] == 'private':
        request = {
            "type": "private",
            "to": msg["sender_email"],
            "content": "[Нажмите сюда, чтобы скачать сформированный файл]({})".format(result["uri"])
        }

        client.send_message(request)

    elif msg["type"] == 'stream':
        request = {
            "type": "stream",
            "to": msg["display_recipient"],
            "topic": msg["subject"],
            "content": "[Нажмите сюда, чтобы скачать сформированный файл]({})".format(result["uri"])
        }

        client.send_message(request)


def get_message(msg):
    if msg["sender_email"] == BOT_MAIL:
        return

    print(msg)

    Schedule.deleteOldTasks()

    words = msg["content"].lower().split()

    if (Users.checkUser(msg["sender_email"])):

        if (msg["type"] == 'private'):

            if ('информация' in words):
                if ('расписание' in words):
                    send_msg(msg, BotInfo.SCHEDULE_INFO)
                elif ('пользователи' in words or 'коллеги' in words or 'люди' in words):
                    send_msg(msg, BotInfo.USER_INFO)
                elif ('документы' in words):
                    send_msg(msg, BotInfo.DOCS_INFO)
                else:
                    send_msg(msg, BotInfo.fullInfo())

            elif ('расписание' in words):
                if (len(words) == 1):
                    send_msg(msg, Schedule.getAllTasks(msg["sender_email"]))
                elif ('сегодня' in words):
                    send_msg(msg, Schedule.getTodayTasks(msg["sender_email"]))
                elif ('добавить' in words):
                    send_msg(msg, Schedule.addTask(msg["sender_email"], words[2:]))
                elif (len(words) == 2):
                    send_msg(msg, Schedule.getTasksByDate(
                        msg["sender_email"], words[1]))
                elif ('на' in words and len(words) == 3):
                    send_msg(msg, Schedule.getTasksByDate(
                        msg["sender_email"], words[2]))
                else:
                    send_msg(msg, BotInfo.DONT_UNDERSTAND_MSG)

            elif ('документы' in words):
                send_msg(msg, BotInfo.DOCS_INFO)

            elif ('выходные' in words):
                if (len(words) == 1):
                    send_msg(msg, Holydays.getResponse())
                elif (len(words) == 2):
                    send_msg(msg, Holydays.getResponse(words[1]))
                else:
                    send_msg(msg, BotInfo.DONT_UNDERSTAND_MSG)

            elif (checkMsgOnDocsName(msg["content"].lower())):
                answer = Docs.messageProcessing(
                    msg["sender_email"], msg["content"])

                if not answer[1]:
                    send_msg(msg, "Документа с таким именем или номером не существует")
                else:
                    if answer[0]:
                        send_file(msg, answer[1])
                    else:
                        send_msg(msg, answer[1])

            else:
                message = UserInfo.getUserInfo(words)
                if not message:
                    send_msg(msg, BotInfo.DONT_UNDERSTAND_MSG)
                else:
                    send_msg(msg, message)

        elif ('@**simpleBot**' in msg["content"] and msg['sender_full_name'] != 'simpleBot'):

            if ('информация' in words):
                if ('расписание' in words):
                    send_msg(msg, BotInfo.SCHEDULE_INFO)
                elif ('пользователи' in words or 'коллеги' in words or 'люди' in words):
                    send_msg(msg, BotInfo.USER_INFO)
                elif ('документы' in words):
                    send_msg(msg, BotInfo.DOCS_INFO)
                else:
                    send_msg(msg, BotInfo.fullInfo())

            elif ('расписание' in words):
                if (len(words) == 2):
                    send_msg(msg, Schedule.getAllTasks(msg["sender_email"]))
                elif ('сегодня' in words):
                    send_msg(msg, Schedule.getTodayTasks(msg["sender_email"]))
                elif ('добавить' in words):
                    send_msg(msg, Schedule.addTask(msg["sender_email"], words[3:]))
                elif (len(words) == 3):
                    send_msg(msg, Schedule.getTasksByDate(
                        msg["sender_email"], words[2]))
                elif ('на' in words and len(words) == 4):
                    send_msg(msg, Schedule.getTasksByDate(
                        msg["sender_email"], words[3]))
                else:
                    send_msg(msg, BotInfo.DONT_UNDERSTAND_MSG)

            elif ('документы' in words):
                send_msg(msg, BotInfo.DOCS_INFO)

            elif ('выходные' in words):
                if (len(words) == 2):
                    send_msg(msg, Holydays.getResponse())
                elif (len(words) == 3):
                    send_msg(msg, Holydays.getResponse(words[2]))
                else:
                    send_msg(msg, BotInfo.DONT_UNDERSTAND_MSG)

            elif (checkMsgOnDocsName(msg["content"].lower())):
                answer = Docs.messageProcessing(
                    msg["sender_email"], msg["content"].replace('@**simpleBot** ', ''))

                if not answer[1]:
                    send_msg(msg, "Документа с таким именем или номером не существует")
                else:
                    if answer[0]:
                        send_file(msg, answer[1])
                    else:
                        send_msg(msg, answer[1])

            else:
                message = UserInfo.getUserInfo(words[1:])
                if not message:
                    send_msg(msg, BotInfo.DONT_UNDERSTAND_MSG)
                else:
                    send_msg(msg, message)
        
    else:

        if (msg["type"] == 'private'):
            if (words[0] == "добавить" and words[1] == "информацию"):
                send_msg(msg, Users.getUserInfo(msg["sender_email"], words[2:]))
            else:
                send_msg(msg, Users.helloMessage())
        
        elif ('@**simpleBot**' in msg["content"] and msg['sender_full_name'] != 'simpleBot'):
            if (words[1] == "добавить" and words[2] == "информацию"):
                send_msg(msg, Users.getUserInfo(msg["sender_email"], words[3:]))
            else:
                send_msg(msg, Users.helloMessage())

# config_file - путь к файлу zuliprc, который содержит 
# все подробности о конфигурации бота
#client = zulip.Client(config_file="/home/path/.zuliprc")

# Функция call_on_each_message() будет выполняться вечно
# А когда боту отправят сообщение, то произойдет вызов 
# функции get_message, в которую передастся содержимое
# и информация о переданном сообщении в формате JSON
client.call_on_each_message(get_message)